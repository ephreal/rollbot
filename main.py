# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
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


def first_time_setup(CONFIG):
    """
    Walks the user through for first time setup.

    CONFIG: JSON dict
        -> TOKEN: str
    """
    token = input("Please input your discord bot token here: ")
    roll_restrict = input("Restrict rolling to rolling channels? y/n: ")
    roll_restrict = roll_restrict.lower().strip()
    print(repr(roll_restrict))
    while not (roll_restrict == 'n') and not (roll_restrict == 'y'):
        roll_restrict = input("Restrict rolling to rolling channels? y/n: ")

    if roll_restrict == "y":
        roll_restrict = True
    else:
        roll_restrict = False

    CONFIG["token"] = token
    CONFIG["roll_restrict"] = roll_restrict

    with open("config/config.json", 'w') as config_file:
        config_file.write(json.dumps(CONFIG, sort_keys=True,
                                     indent=4, separators=(',', ': ')))

    return token, roll_restrict


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
ROLL_RESTRICT = CONFIG["restrict_rolling"]

if TOKEN == "YOUR_BOT_TOKEN_HERE":
    TOKEN, ROLL_RESTRICT = first_time_setup(CONFIG)

while not os.path.exists("poweroff"):
    BOT = bot.build_bot(PREFIX, DESC, ROLL_RESTRICT)
    run_client(BOT, TOKEN)
    importlib.reload(bot)

# Remove the file "poweroff" so it'll turn on next time
os.remove("poweroff")
sys.exit()
