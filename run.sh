#!/bin/bash

kill -9 \
    "$(ps -ef | grep "/bin/python3 $HOME/scripts/bin/translate/translate.py" |\
    sed 2d |\
    awk '{print $2}')" && notify-send -r 9526 "󰊿 Close Translations" ||\
    ~/scripts/bin/translate/translate.py
