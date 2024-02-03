from abc import abstractmethod
from typing import Any, Callable, Coroutine, Dict, Protocol, runtime_checkable


@runtime_checkable
class Translator(Protocol):
    @abstractmethod
    async def Do(self, text: str) -> Dict[str, str]:
        pass


class Mouser(Protocol):
    @abstractmethod
    def listen(self, on_click: Callable[[], Coroutine[Any, Any, None]]) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass


class Notifyer(Protocol):
    @abstractmethod
    def send(self, title: str, body: str) -> None:
        pass


class Clipboarder(Protocol):
    @abstractmethod
    def get(self) -> str:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

class Comparable(Protocol):
    @abstractmethod
    def __eq__(self, __value) -> bool:
        pass


class Ord(Comparable, Protocol):
    @abstractmethod
    def __le__(self, __value) -> bool:
        pass

    @abstractmethod
    def __lt__(self, __value) -> bool:
        pass

    @abstractmethod
    def __ge__(self, __value) -> bool:
        pass

    @abstractmethod
    def __gt__(self, __value) -> bool:
        pass
