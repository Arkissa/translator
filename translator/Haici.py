from typing import Any, Dict
from urllib.parse import quote_plus
from requests import Response
from httpclient import Session
from lxml import etree


class Haici:
    def __init__(self, proxy: dict[str, str] = {}) -> None:
        self.__body: Dict[str, Any] = {
            "method": "get",
            "timeout": 5,
            "proxies": proxy,
        }
        self.__url: str = "https://apii.dict.cn/mini.php?q={}"

    async def Do(self, text: str) -> Dict[str, str]:
        def handle(response: Response) -> Dict[str, str]:
            text = response.text

            haici = etree.HTML(text).xpath("/html/body/div[1]/text()")
            haici = haici if isinstance(haici, list) else []

            return  {
                "<b>󰭻 Haici</b>\n": "\n".join([i for i in haici if isinstance(i, str)])
            } if haici else {}

        return Session().Request(handle, {
            **self.__body,
            "url": self.__url.format(quote_plus(text))
        })
