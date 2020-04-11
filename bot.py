# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""


import os
import traceback

from datetime import datetime
from discord import Game
from discord.ext import commands


def build_bot(prefix, description="Rollbot"):

    BOT = commands.Bot(command_prefix=prefix,
                       description=description)

    @BOT.event
    async def on_member_join(member):
        await member.send("Welcome to our server. Please be kind and "
                          "courteous. If you wish to test the bots, please ask"
                          " to be given the bot testing role.")

    @BOT.event
    async def on_ready():
        """
        Post setup hook.
        Initializes any necessary variables and sets the played game to
        a message on how to get help.
        """
        # Initialize needed variables
        # initialize music players dict
        BOT.players = {}

        # Uptime statistic
        BOT.boot_time = datetime.now()

        # Load all cogs
        print("Startup complete, loading Cogs....")
        await load_cogs()
        print("Cog loading complete.")
        print("Connected to server and awaiting commands.")

        # Set help message
        help_message = Game(name=f"message '{prefix}help' for help")
        if not hasattr(BOT, 'appinfo'):
            BOT.appinfo = await BOT.application_info()
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
                                       "endorsement of the sentiments "
                                       "expressed in said message. Any "
                                       "statements claiming my endorsing of "
                                       "this message implies that I agree "
                                       "with said message is taken horribly "
                                       "out of context.")

            await message.add_reaction('👍')

        if message.content.startswith(prefix):
            await BOT.process_commands(message)

    async def load_cogs(unload_first=False):
        """
        Handles loading all cogs in for the bot.
        """

        cogs = [cog for cog in os.listdir('cogs')
                if os.path.isfile(f"cogs/{cog}")]

        cogs = [cog.replace(".py", "") for cog in cogs]

        for extension in cogs:
            try:
                print(f"Loading {extension}...")
                BOT.load_extension(f"cogs.{extension}")
                print(f"Loaded {extension}")

            except AttributeError as e:
                print(f"Cog {extension} is malformed. Do you have a setup"
                      "function?")
                traceback.print_tb(e.__traceback__)

            except ModuleNotFoundError:
                print(f"Could not find {extension}. Please make sure it "
                      "exists.")

            except OSError as lib_error:
                print("Opus is probably not installed")
                print(f"{lib_error}")

            except commands.errors.ExtensionAlreadyLoaded:
                print(f"The cog {extension} is already loaded.\n"
                      "Skipping the load process for this cog.")

            except SyntaxError as e:
                print(f"The cog {extension} has a syntax error.")
                traceback.print_tb(e.__traceback__)

            except commands.errors.NoEntryPoint as e:
                print(f"Cog {extension} has no setup function.")
                traceback.print_tb(e.__traceback__)

    return BOT


if __name__ == "__main__":
    import sys
    print("The bot must be ran through main.py")
    print("Please run 'python main.py' instead")
    sys.exit()
