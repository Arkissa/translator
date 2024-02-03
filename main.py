#!/bin/python3
import argparse
import asyncio
from translate import Translate
from tools import Display

def main(args: argparse.Namespace):
    display = Display(args.display)

    if args.listen:
        from signal import SIGINT, signal
        from tools import mouse, clipboard

        m, c = mouse(), clipboard()
        def handle(x, y) -> None:
            _, _ = x, y
            c.close()
            m.close()

        signal(SIGINT, handle)

        async def on_click() -> None:
            text = c.get()               \
                    .strip()             \
                    .replace("\n", "")   \
                    .replace("\r", "")

            if text == "":
                return

            display.Do(text)
            display.Do(await Translate(args.proxy).Do(text))

        m.listen(on_click)
    else:
        display.Do(args.text)
        async def run():
            display.Do(await Translate(args.proxy).Do(args.text))

        asyncio.run(run())

if __name__ == "__main__":
    parse = argparse.ArgumentParser(description="Translate between English and Chinese.",
                                    add_help=True)
    group = parse.add_mutually_exclusive_group(required=True)
    group.add_argument("-t", "--text",
                      help="Text to translate.",
                      type=str)
    group.add_argument("-l", "--listen",
                       help="Enable listening mode, translate the text selected bythe mouse. (default: disable)",
                       action="store_true",
                       default=False)
    parse.add_argument("-p", "--proxy",
                       help="Set request proxy URL (default: empty)",
                       default="",
                       type=str)
    parse.add_argument("-d", "--display",
                       help="Set translation result display style. (default: text)",
                       choices=["text", "json", "notify"],
                       default="text",
                       type=str)

    main(parse.parse_args())
    
