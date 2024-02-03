from typing import Any, Dict, Callable
from requests import Session as session, Response
from tools import singleton


@singleton
class Session:
    def __init__(self) -> None:
        self.__client = session()
        self.__headers = {
                    "User-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, "
                                  "like Gecko) Chrome/108.0.0.0 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.5",
                }

    def Request(self,
                handle: Callable[[Response], Dict[str, str]],
                body: Dict[str, Any]
               ) -> Dict[str, str]:

        try:
            response = self.__client.request(**{
                **body,
                "headers": self.__headers
            })

            if not response or response.status_code != 200:
                raise Exception(body["url"] + " http request error")

            return handle(response)
        except Exception:
            return {}

