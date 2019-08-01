# -*- coding: utf-8 -*-

"""
Copyright 2018 Ephreal

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import asyncio
import bot
import importlib
import json
import os
import sys


def load_config():
    """
    Loads bot configuration for use.
    """
    with open("config/config.json", 'r') as config_file:
        return json.load(config_file)


def run_client(client, *args, **kwargs):
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(client.start(*args, **kwargs))
    except Exception as e:
        print("Error", e)
    print("Restarting...")


CONFIG = load_config()
TOKEN = CONFIG["token"]
PREFIX = CONFIG["prefix"]
DESC = CONFIG["description"]

while not os.path.exists("poweroff"):
    BOT = bot.build_bot(PREFIX, DESC)
    run_client(BOT, TOKEN)
    importlib.reload(bot)

# Remove the file "poweroff" so it'll turn on next time
os.remove("poweroff")
sys.exit()