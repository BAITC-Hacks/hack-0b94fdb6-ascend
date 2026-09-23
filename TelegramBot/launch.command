#!/bin/zsh
set -eu
cd -- "${0:A:h:h}"
python3 -m TelegramBot.launch
