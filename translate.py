#!/bin/python

import requests
import subprocess
import asyncio
from urllib.parse import quote_plus
from lxml import etree


class misc:
    def __init__(self) -> None:
        self.mouse = open("/dev/input/mice", "rb")

    def bindLeft(self) -> int:
        return self.mouse.read(3)[0] & 0x1

    def close(self):
        self.mouse.close()


class clip:
    def copy(self) -> None:
        subprocess.Popen(
            ["xclip", "-selection", "p"], stdin=subprocess.PIPE, close_fds=True
        ).communicate(input="".encode())

    def paste(self) -> str:
        out, err = subprocess.Popen(
            ["xclip", "-selection", "p", "-o"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            close_fds=True,
        ).communicate()
        return out.decode() + err.decode()


class trans:
    def __init__(self) -> None:
        self.request = requests.Session()
        self.url = {
            "google": "https://translate.google.com/translate_a/single?client=gtx&sl=auto&tl={}&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&q={}",
            "haici": "https://apii.dict.cn/mini.php?q=",
            "youdao": "https://dict.youdao.com/jsonapi_s?doctype=json&jsonversion=4",
            "baidu": "https://fanyi.baidu.com/sug",
        }
        self.headers = {
            "User-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        }

    async def google(self, text):
        t, num = "", 0
        for t in text:
            if ord(t) > 255:
                num += 1
            else:
                num -= 1

        tl = num <= 0 and "zh-CN" or "en"
        try:
            response = self.request.get(
                self.url["google"].format(tl, quote_plus(text)),
                headers=self.headers,
                timeout=5,
            )
            if not response or response.status_code != 200:
                return

            fanyi = response.json()

            t = fanyi[0][0] and f"<b>󰭻 Google</b>\n{fanyi[0][0][0]}\n" or ""
        except Exception:
            t = ""
            pass

        return t

    async def haici(self, text):
        t = ""
        try:
            response = self.request.get(
                self.url["haici"] + quote_plus(text), headers=self.headers, timeout=5
            )
            if not response or response.status_code != 200:
                return

            html = etree.HTML(response.text)
            haici = html.xpath("/html/body/div[1]/text()")
            t = haici and "<b>󰭻 Haici</b>\n" + "\n".join(haici) + "\n" or ""
        except Exception:
            pass

        return t

    async def youdao(self, text):
        t = ""
        youdao = []
        body = {"q": text, "client": "web", "keyfrom": "webdict"}
        try:
            response = self.request.post(
                self.url["youdao"],
                headers=self.headers,
                timeout=5,
                data=body,
            )
            if not response or response.status_code != 200:
                return

            fanyi = response.json()

            if "fanyi" in fanyi:
                t = "<b>󰭻 Youdao</b>\n" + fanyi["fanyi"]["tran"]
            else:
                for value in fanyi["web_trans"]["web-translation"][0]["trans"]:
                    youdao.append(value["value"])
                t = youdao and "<b>󰭻 Youdao</b>\n" + "\n".join(youdao) + "\n" or ""
        except Exception:
            pass

        return t

    async def baidu(self, text):
        t = ""
        baidu = []
        body = {"kw": f"{text}"}
        try:
            response = self.request.post(
                self.url["baidu"], headers=self.headers, data=body, timeout=5
            )
            if not response or response.status_code != 200:
                return

            fanyi = response.json()
            for value in fanyi["data"]:
                baidu.append(value["k"] + " " + value["v"])
            t = baidu and "<b>󰭻 Baidu</b>\n" + "\n".join(baidu) + "\n" or ""
        except Exception:
            pass

        return t


def notify(title: str, msg: str, id: int):
    msg = msg.replace("'", "\\'").replace('"', '\\"')
    subprocess.Popen(["/bin/bash", "-c", f'notify-send -r {id} "{title}" "{msg}"'])


async def main(mouse: misc, translating: trans, c: clip):
    notify("󰊿 Open Translations", "", 9526)
    n, read = 0, False
    while True:
        while mouse.bindLeft() == 1:
            if n >= 1:
                n = 0
                read = True
            n += 1

        if not read:
            c.copy()
            continue
        else:
            read = False
        text = c.paste()
        text = text.replace("\n", "").replace("\r", "")
        if text == "":
            continue

        notify("󱅫 Start Translating", f"{text}", 9526)
        results = await asyncio.gather(
            translating.google(text),
            translating.haici(text),
            translating.youdao(text),
            translating.baidu(text),
        )
        trans_text = ""
        for i in results:
            trans_text += isinstance(i, str) and i or ""

        if trans_text == "":
            trans_text = "translating to error....please check your network"
        notify("󰊿 Translate", trans_text, 9526)


if __name__ == "__main__":
    mouse = misc()
    translating = trans()
    asyncio.run(main(mouse, translating, clip()))
    mouse.close()
