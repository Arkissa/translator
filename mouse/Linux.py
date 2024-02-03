import asyncio
from time import sleep
from typing import Any, Callable, Coroutine, Dict


class Linux:
    def __init__(self) -> None:
        self._mouse  = open("/dev/input/mice", "rb")
        self._closed = False


    def listen(self, on_click: Callable[[], Coroutine[Any, Any, Dict[str, str]]]) -> None:
        count = 0
        while not self._closed:
            while self._mouse.read(3)[0] & 1:
                count += 1
            
            if count > 1:
                asyncio.run(on_click())
            
            count = 0
            sleep(0.1)

        self._mouse.close()

    def close(self) -> None:
        self._closed = True
