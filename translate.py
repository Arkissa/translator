from asyncio import gather
from tools import _LOADMODULE
from os import listdir
from interface import Translator
from tools import (
    isPyFile,
    proxy,
    Filter,
    Map,
    singleton,
    dropWhileEnd,
)
from typing import Any, Callable, Coroutine, Dict, List


@singleton
class Translate:
    def __init__(self, proxy_url: str="") -> None:
        def dropPy(s: str) -> str:
            return dropWhileEnd(lambda x: x == ".", s)

        def loadMod(s: str) -> Any:
            return getattr(_LOADMODULE(f"translator.{s}"), s)
        
        def instance(obj: Any) -> Any:
            return obj(proxy(proxy_url))

        def isTranslator(obj: Any) -> bool:
            return isinstance(obj, Translator)

        def toTranslator(obj: Any) -> Translator:
            return obj

        def toAsync(obj: Translator) -> Callable[[str], Coroutine[Any, Any, Dict[str, str]]]:
            return obj.Do

        self.__modules = list(Map(toAsync) \
                             (Map(toTranslator) \
                             (Filter(isTranslator) \
                             (Map(instance) \
                             (Map(loadMod) \
                             (Map(dropPy) \
                             (Filter(isPyFile) \
                             (listdir("translate")))))))))


    async def Do(self, text: str) -> List[Dict[str, str]]:
        return [] if text == '' else await gather(*map(lambda f: f(text), self.__modules))
