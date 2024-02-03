import subprocess


class Linux:
    def __init__(self) -> None:
        pass

    def send(self, title: str, body: str) -> None:
        body = body.replace("'", "\\'").replace('"', '\\"')
        subprocess.Popen(["/bin/bash", "-c", f'notify-send -r 9527 "{title}" "{body}"'])
