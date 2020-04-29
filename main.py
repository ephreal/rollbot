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
    restrict_rolling = input("Restrict rolling to rolling channels? y/n: ")
    restrict_rolling = restrict_rolling.lower().strip()
    while not (restrict_rolling == 'n') and not (restrict_rolling == 'y'):
        restrict_rolling = input("Restrict rolling to rolling channels? y/n: ")

    catapi_key = input("Enter your catapi API key now. If you have none, just"
                       "hit enter: ")

    if restrict_rolling == "y":
        restrict_rolling = True
    else:
        restrict_rolling = False

    CONFIG["token"] = token
    CONFIG["restrict_rolling"] = restrict_rolling
    CONFIG["catapi_key"] = catapi_key

    with open("config/config.json", 'w') as config_file:
        config_file.write(json.dumps(CONFIG, sort_keys=True,
                                     indent=4, separators=(',', ': ')))

    return token, restrict_rolling


def run_client(client, *args, **kwargs):
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(client.start(*args, **kwargs))
    except Exception as e:
        print("Error", e)
    print("Restarting...")


CONFIG = load_config()
TOKEN = CONFIG["token"]

if TOKEN == "YOUR_BOT_TOKEN_HERE":
    TOKEN, ROLL_RESTRICT = first_time_setup(CONFIG)

PREFIX = CONFIG["prefix"]
DESC = CONFIG["description"]
ROLL_RESTRICT = CONFIG["restrict_rolling"]
CATAPI_KEY = CONFIG["catapi_key"]

while not os.path.exists("poweroff"):
    BOT = bot.build_bot(PREFIX, ROLL_RESTRICT, DESC, CATAPI_KEY)
    run_client(BOT, TOKEN)
    importlib.reload(bot)

# Remove the file "poweroff" so it'll turn on next time
os.remove("poweroff")
sys.exit()
