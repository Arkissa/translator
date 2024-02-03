import subprocess
from tools import singleton


@singleton
class Linux:
    def __init__(self) -> None:
        pass
        

    def get(self) -> str:
        out, err = subprocess.Popen(
            ["xclip", "-selection", "p", "-o"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            close_fds=True,
        ).communicate()
       
        subprocess.Popen(
            ["xclip", "-selection", "p"],
            stdin=subprocess.PIPE,
            close_fds=True
        ).communicate(input="".encode())
        return out.decode() + err.decode()

    def close(self) -> None:
        pass
