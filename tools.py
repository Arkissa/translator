from collections.abc import Iterable
from importlib import import_module
import json
from platform import system
from typing import Dict, Callable, List, TypeVar, Union
from interface import Notifyer, Ord, Clipboarder, Mouser

_SYSTEM = system()
_LOADMODULE = import_module

def clipboard() -> Clipboarder:
    return getattr(_LOADMODULE(f"clipboard.{_SYSTEM}"), _SYSTEM)()

def mouse() -> Mouser:
    return getattr(_LOADMODULE(f"mouse.{_SYSTEM}"), _SYSTEM)()

def notify() -> Notifyer:
    return getattr(_LOADMODULE(f"notify.{_SYSTEM}"), _SYSTEM)()

def singleton(cls):
    instance = {}
    def f(*args, **kvargs):
        if cls in instance:
            return instance[cls]
        else:
            instance[cls] = cls(*args, **kvargs)
            return instance[cls]

    return f

_FT = TypeVar("_FT", bound=Ord)
def Filter(f: Callable[[_FT], bool]) -> Callable[[Iterable[_FT]], Iterable[_FT]]:
    return lambda x: filter(f, x)

_T = TypeVar("_T")
_R = TypeVar("_R")
def Map(f: Callable[[_T], _R]) -> Callable[[Iterable[_T]], Iterable[_R]]:
    return lambda x: map(f, x)

def proxy(url: str) -> Dict[str, str]:
    return {"http": url, "https": url} if url else {}

def isPyFile(file: str) -> bool:
    return file.endswith(".py")

def dropWhileEnd(f: Callable[[str], bool], s: str) -> str:
    if s == "":
        raise ValueError("not found substring")

    if f(s[-1]):
        return s[:-1]
    
    return dropWhileEnd(f, s[:-1])


class Display:
    def __init__(self, show: str) -> None:
        self.__do: Callable[[Union[List[Dict[str, str]], str]], None]
        match show:
            case "notify":
                n = notify()
                self.__do = lambda xs: n.send("󰊿 Start Translate", xs) \
                            if isinstance(xs, str) \
                            else n.send("󰊿 Translate", "\n".join(map(lambda x: "".join(x.popitem()),
                                                                 filter(lambda x: len(x), xs))))
            case "json":
                self.__do = lambda xs: print(json.dumps({"text": xs})) \
                            if isinstance(xs, str) \
                            else print(json.dumps([x for x in xs if len(x)]))
            case _:
                self.__do = lambda xs: print(f"[Start Translate: \"{xs}\"]") \
                            if isinstance(xs, str) \
                            else print("\n".join(map(lambda x: "".join(x.popitem()),
                                                 filter(lambda x: len(x), xs))))


    def Do(self, xs: List[Dict[str, str]] | str) -> None:
        self.__do(xs)
