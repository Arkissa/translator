from typing import Any, Dict
from urllib.parse import quote_plus
from requests import Response
from httpclient import Session


class Google:
    def __init__(self, proxy: Dict[str, str] = {}) -> None:
        self.__body: Dict[str, Any] = {
            "method": "get",
            "timeout": 5,
            "proxies": proxy,
        }
        self.__url: str = "https://translate.google.com/translate_a/single?client=gtx&sl=auto&tl={}&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&q={}"

    def __lang(self, text: str):
        return sum(ord(i) > 254 and 1 or -1 for i in text) <= 0 and "zh-CN" or "en"


    async def Do(self, text: str) -> Dict[str, str]:
        def handle(response: Response) -> Dict[str, str]:
            text = response.json()

            return  {
                "<b>󰭻 Google</b>\n": "".join(
                        filter(lambda x: x is not None,
                               [i[0] for i in text[0] if isinstance(i, list)]
                        )
                    )
                } if text[0][0] else {}
        
        return Session().Request(handle, {
            **self.__body,
            "url": self.__url.format(self.__lang(text), quote_plus(text.replace("\n", "+")))
        })
