from typing import Dict, Any
from requests import Response
from httpclient import Session


class Youdao:
    def __init__(self, proxy: Dict[str, str] = {}) -> None:
        self.__body: Dict[str, Any] = {
            "method":  "post",
            "timeout": 5,
            "proxies": proxy,
            "url": "https://dict.youdao.com/jsonapi_s?doctype=json&jsonversion=4"
        }

    async def Do(self, text: str) -> Dict[str, str]:
        def handle(response: Response) -> Dict[str, str]:
            text = response.json()
            if "fanyi" in text:
                return {"<b>󰭻 Youdao</b>\n": text["fanyi"]["tran"]}

            if "web_trans" not in text:
                return {}

            youdao = [value["value"] for value in text["web_trans"]["web-translation"][0]["trans"]]
            return {"<b>󰭻 Youdao</b>\n": "\n".join(youdao) } if youdao else {}

        return Session().Request(handle, {
            **self.__body,
            "data": {"q": text, "client": "web", "keyfrom": "webdict"}
        })
