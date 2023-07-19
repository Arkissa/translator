#!/bin/python

import sys
from typing import Any, Dict, Callable, Tuple
import requests
import subprocess
import asyncio
import signal
from urllib.parse import quote_plus
from lxml import etree

TIMEOUT = 5
CAN_RUN = True
REQUEST = requests.Session()
ERR_NETWORK = "translating to error....please check your network"
URL = {
    "google": "https://translate.google.com/translate_a/single?client="
              "gtx&sl=auto&tl={}&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt="
              "rw&dt=rm&dt=ss&dt=t&q={}",
    "haici": "https://apii.dict.cn/mini.php?q={}",
    "youdao": "https://dict.youdao.com/jsonapi_s?doctype=json&jsonversion=4",
    "baidu": "https://fanyi.baidu.com/sug",
}
HEADERS = {
    "User-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, "
                  "like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

def mouse() -> Tuple[Callable[[], bytes | int], Callable[[], None]]:
    mice = open("/dev/input/mice", "rb")
    return (
        lambda : mice.read(3)[0] & 0x1 if not mice.closed else 0,
        lambda : mice.close(),
    )

def copy() -> None:
        subprocess.Popen(
            ["xclip", "-selection", "p"], stdin=subprocess.PIPE, close_fds=True
        ).communicate(input="".encode())

def paste() -> str:
        out, err = subprocess.Popen(
            ["xclip", "-selection", "p", "-o"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            close_fds=True,
        ).communicate()
        return out.decode() + err.decode()

def http(
        handle: Callable[[requests.Response], Any],
        body: Dict[str, Any],
) -> (
        Dict[str, str] | str
):

    t = ""
    try:
        response = REQUEST.request(**body)
        if not response or response.status_code != 200:
            raise requests.Timeout

        t = handle(response)
    except Exception:
        pass

    return t

def check_lang(text: str) -> str:
    return sum(ord(i) > 254 and 1 or -1 for i in text) <= 0 and "zh-CN" or "en"

async def google(text: str, proxy: dict[str, str] = {}) -> Dict[str, str] | str:
    body = {
        "method": "get",
        "url": URL["google"].format(check_lang(text), quote_plus(text)),
        "headers": HEADERS,
        "timeout": TIMEOUT,
        "proxies":proxy,
    }

    return http(google_fanyi, body)

def google_fanyi(fanyi: requests.Response) -> Dict[str, str] | str:
    text = fanyi.json()

    return  text[0][0] and {"<b>󰭻 Google</b>\n": text[0][0][0] + "\n"} or ""


async def haici(text: str, proxy: dict[str, str] = {}) -> Dict[str, str] | str:
    body = {
        "method": "get",
        "url": URL["haici"].format(quote_plus(text)),
        "headers": HEADERS,
        "timeout": TIMEOUT,
        "proxies": proxy,
    }

    return http(haici_fanyi, body)

def haici_fanyi(fanyi: requests.Response) -> Dict[str, str] | str:
    text = fanyi.text

    haici = etree.HTML(text).xpath("/html/body/div[1]/text()")
    haici = haici if isinstance(haici, list) else []

    return  {
        "<b>󰭻 Haici</b>\n": "\n".join([i for i in haici if isinstance(i, str)]) + "\n"
    } if haici else ""

async def youdao(text: str, proxy: dict[str, str] = {}) -> Dict[str, str] | str:
    body = {
        "method":  "post",
        "url":     URL["youdao"],
        "proxies": proxy,
        "headers": HEADERS,
        "timeout": TIMEOUT,
        "data":    {"q": text, "client": "web", "keyfrom": "webdict"},
    }
    
    return http(youdao_fanyi, body)

def youdao_fanyi(fanyi: requests.Response) -> Dict[str, str] | str:
    text = fanyi.json()
    if "fanyi" in text:
        return {"<b>󰭻 Youdao</b>\n": text["fanyi"]["tran"]}

    youdao = [value["value"] for value in text["web_trans"]["web-translation"][0]["trans"]]
    return {"<b>󰭻 Youdao</b>\n": "\n".join(youdao) } if youdao else ""

async def baidu(text: str, proxy: dict[str, str] = {}) -> Dict[str, str] | str:
    body = {
        "method":  "post",
        "url":     URL["baidu"],
        "headers": HEADERS,
        "timeout": TIMEOUT,
        "proxies": proxy,
        "data":    {"kw": text},
    }

    return http(baidu_fanyi, body)

def baidu_fanyi(fanyi: requests.Response) -> Dict[str, str] | str:
    text = fanyi.json()

    baidu = [value["k"] + " " + value["v"] for value in text["data"]]
    return {"<b>󰭻 Baidu</b>\n" : "\n".join(baidu) + "\n"} if baidu else ""

def notify(title: str, msg: str, id: int) -> None:
    msg = msg.replace("'", "\\'").replace('"', '\\"')
    subprocess.Popen(["/bin/bash", "-c", f'notify-send -r {id} "{title}" "{msg}"'])

def handle_signal(signum: Any, frame: Any) -> None:
    _, _ = signum, frame
    global CAN_RUN
    CAN_RUN = False

def handle_proxy(proxy: str) -> dict[str, str]:
    return proxy and {"http": proxy, "https": proxy} or {}

async def main(left: Callable[[], bytes | int], proxy: str):
    notify("󰊿 Open Translations", "", 9526)
    n, read = 0, False
    while CAN_RUN:
        while left() == 1:
            if n >= 1:
                n = 0
                read = True
            n += 1

        if not read:
            copy()
            continue

        read = False
        text = paste().replace("\n", "").replace("\r", "")
        if text == "":
            continue

        notify("󱅫 Start Translating", text, 9526)
        results = await asyncio.gather(
            google(text, handle_proxy(proxy)),
            youdao(text, handle_proxy(proxy)),
            haici(text, handle_proxy(proxy)),
            baidu(text, handle_proxy(proxy)),
        )
        print(results)
        
        answer = [
            "".join(
                [k + v for k, v in i.items() if isinstance(k, str) and isinstance(v, str)]
            )
            for i in results if isinstance(i, dict)
        ]

        notify("󰊿 Translate", "\n".join(answer) if answer else ERR_NETWORK, 9526)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_signal)
    left, close = mouse()
    asyncio.run(main(
        left,
        len(sys.argv) == 2 and sys.argv[1] or ""),
    )

    close()
