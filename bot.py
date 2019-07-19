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
import traceback

from discord.ext import commands
from discord import Game
from subprocess import PIPE, Popen


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


@BOT.event
async def on_message(message):
    """
    Generic operations on user message. For example, adding to analytics to
    see if users are active on the guild.
    """

    if message.author.bot:
        return

    if "+endorse" in message.content:
        bot_nick = message.guild.me.nick
        await message.channel.send(f"My name is {bot_nick}, and I endorse "
                                   "the above message.\nNote that my "
                                   "endorsement in no way reflects the "
                                   "opinions of me or my creator, does "
                                   "not make any guarantee about the "
                                   "correctness of said message, and "
                                   "may, in fact, not be an actual "
                                   "endorsement of the sentiments expressed "
                                   "in said message. Any statements claiming "
                                   "my endorsing of this message implies "
                                   "that I agree with said message is taken "
                                   "horribly out of context.")

        await message.add_reaction('👍')

    if message.content.startswith(CONFIG["prefix"]):
        await BOT.process_commands(message)


async def load_cogs(unload_first=False):
    """
    Handles loading all cogs in for the bot.
    """

    cogs = [
        "cogs.admin",
        "cogs.characters",
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
        for cog in cogs:
            try:
                print(f"Unloading {cog}")
                BOT.unload_extension(cog)
            except commands.errors.ExtensionNotLoaded:
                print(f"Cog {cog} is already unloaded.")

    for extension in cogs:
        try:
            print(f"Loading {extension}...")
            BOT.load_extension(f"{extension}")
            print(f"Loaded {extension.split('.')[-1]}")

        except ModuleNotFoundError:
            print(f"Could not find {extension}. Please make sure it exists.")

        except OSError as lib_error:
            print("Opus is probably not installed")
            print(f"{lib_error}")

        except commands.errors.ExtensionAlreadyLoaded:
            print(f"The cog {extension} is already loaded.\n"
                  "Skipping the load process for this cog.")

        except SyntaxError as e:
            print(f"The cog {extension} has a syntax error.")
            traceback.print_tb(e.__traceback__)


@BOT.command(hidden=True)
async def reload(ctx):
    """
    Handles reloading all cogs which allows live updates.
    """

    cmd = Popen("git pull", stdout=PIPE)
    out, _ = cmd.communicate()

    await load_cogs(unload_first=True)
    await ctx.send("Reloaded")


BOT.run(CONFIG["token"])
