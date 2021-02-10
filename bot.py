# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""


import os
import traceback
import json
import re

from datetime import datetime
from discord import Game
from discord.ext import commands
from utils.message_builder import on_join_builder
from utils.db import db_migration_handler
from utils.handlers import db_handler


def build_bot(prefix, restrict_rolling, description, catapi_key=None):

    BOT = commands.Bot(command_prefix=prefix, description=description)

    with open("utils/json/shadowland.json", "r") as f:
        BOT.shadowland_strings = json.loads(f.read())

    @BOT.event
    async def on_member_join(member):
        guild = member.guild.id
        if await BOT.db_handler.guilds.get_greeting_status(guild):
            message = await BOT.db_handler.guilds.get_greeting(guild)
            message = await on_join_builder(member, message)
            await member.send(embed=message)

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

        # Whether or not rolling is restricted to rolling channels only
        BOT.restrict_rolling = restrict_rolling

        # Add in the database handlers
        await database_migrations()
        BOT.db_handler = db_handler.DBHandler()
        BOT.catapi_key = catapi_key

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

        with open("utils/json/excuses.json", "r") as f:
            BOT.excuses = json.loads(f.read())['excuses']

    async def database_migrations():
        """
        Ensures that the bot updates to the most recent database schema
        """

        handler = db_migration_handler.DBMigrationHandler()
        handler.prepare_next_migration()

        choice = "n"

        if handler.current_version != -1:
            print("There are updates available for the bot database.")
            print(f"Issues if not upgraded: {handler.migration.breaks}")
            choice = input("Would you like to upgrade? y/n\n")

        if choice.lower() == "y":
            while handler.current_version != -1:
                print("\n-----------------------------------------------")
                print(f"Updating to version {handler.migration.version}")
                print(f"Description: {handler.migration.description}")
                print(f"Issues if not updated: {handler.migration.breaks}")
                print("-----------------------------------------------\n")
                handler.migrate()
                handler.prepare_next_migration()

    @BOT.event
    async def on_message(message):
        """
        Generic operations on user message. For example, adding to analytics to
        see if users are active on the guild.
        """

        if message.author.bot:
            return

        if message.content.startswith(f"{BOT.command_prefix*2}"):
            return

        if message.content.startswith(prefix):
            await BOT.process_commands(message)
            command = message.content.split()
            command = command[0].replace(BOT.command_prefix, "")
            await BOT.db_handler.metrics.update_commands(command, 1)

        commands = re.findall("{%(.*?)%}", message.content)
        if commands:
            for command in commands:
                command = command.strip()
                if not command.startswith(BOT.command_prefix):
                    command = BOT.command_prefix + command
                message.content = command
                await BOT.process_commands(message)

    @BOT.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            handler = BOT.db_handler.tags
            cmd = "".join(ctx.message.content)[1:]
            await BOT.db_handler.metrics.update_commands(cmd, -1)

            # Try get a normal tag
            content = await handler.fetch_tag(ctx.author.id, cmd)
            if content:
                return await ctx.send(content)

            # Try get a guild tag
            content = await handler.fetch_guild_tag(ctx.guild.id, cmd)
            if content:
                return await ctx.send(content)

            else:
                await ctx.channel.send("https://http.cat/404.jpg")
        else:
            await ctx.send(error)

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
