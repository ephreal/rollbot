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


import json

from discord.ext import commands
from discord import Game


def load_config():
    """
    Loads bot configuration for use.
    """
    with open("config/config.json", 'r') as config_file:
        return json.load(config_file)


CONFIG = load_config()

BOT = commands.Bot(command_prefix=CONFIG["prefix"],
                   description="rollbot")


@BOT.event
async def on_ready():
    """
    Post setup hook.
    Currently lets you know the bot is running
    and sets the played game to a message on
    how to get help.
    """
    print("Startup complete, loading Cogs....")
    await load_cogs()
    print("Cog loading complete.")
    print("Connected to server and awaiting commands.")
    help_message = Game(name=f"message '{CONFIG['prefix']}help' for help")
    await BOT.change_presence(activity=help_message)


async def load_cogs(unload_first=False):
    """
    Handles loading all cogs in for the bot.
    """

    modules = [
        "cogs.admin",
        # "cogs.audio",
        "cogs.dnd",
        "cogs.games",
        "cogs.roller",
        "cogs.shadowrun",
        "cogs.tests",
        "cogs.utils",
        "cogs.vampire",
        ]

    if unload_first:
        for cog in modules:
            BOT.unload_extension(cog)

    for extension in modules:
        try:
            print(f"Loading {extension}...")
            BOT.load_extension(f"{extension}")
            print(f"Loaded {extension.split('.')[-1]}")

        except ModuleNotFoundError as module_error:
            print(f"Failed to load {extension}")
            print("Error follows:\n")
            print(f"{module_error}\n")

        except OSError as lib_error:
            print("Opus is probably not installed")
            print(f"{lib_error}")


@BOT.command(hidden=True)
async def reload(ctx):
    """
    Handles reloading all cogs which allows live updates.
    """
    await load_cogs(unload_first=True)
    await ctx.send("Reloaded")


BOT.run(CONFIG["token"])
