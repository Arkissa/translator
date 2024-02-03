from typing import Dict
from requests import Response
from httpclient import Session


class Baidu:
    def __init__(self, proxy: Dict[str, str] = {}) -> None:
        self.__body: Dict[str, str | int | Dict[str, str]] = {
            "method":  "post",
            "timeout": 5,
            "proxies": proxy,
            "url": "https://fanyi.baidu.com/sug"
        }

    async def Do(self, text: str) -> Dict[str, str]:
        def handle(response: Response) -> Dict[str, str]:
            text = response.json()

            baidu = [value["k"] + " " + value["v"] for value in text["data"]]
            return {"<b>󰭻 Baidu</b>\n" : "\n".join(baidu) + "\n"} if baidu else {}

        return Session().Request(handle, {
            **self.__body,
            "data":    {"kw": text},
        })
