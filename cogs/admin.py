# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

import os
import traceback

from asyncio import sleep
from classes import analytics
from discord import client
from discord.ext import commands
from utils import admin_utils
from utils.checks import check_author
from utils.message_builder import on_join_builder


class admin(commands.Cog):
    """
    Available commands
    .greeting
    .git
    .halt
    .leave
    .logging
    .member_activity
    .reboot
    .reload
    .rename
    .spam
    """
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db_handler.guilds
        self.analytics = analytics.GuildAnalytics()
        self.prefix = {self.bot.command_prefix}
        admin_utils.setup_logging(bot)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def git(self, ctx):
        """
        Pulls changes from github.

        usage:
            .git
        """

        await ctx.send(await admin_utils.git_pull())

    @commands.command(description="Toggle server greeting")
    @commands.has_permissions(administrator=True)
    async def greeting(self, ctx, setting):
        """Server Greeting options

        You can toggle the bot message to users joining the guild here.
        Valid options: on or off

        You can also personalize the greeting the bot sends to anyone joining
        the guild.

        Examples
        --------

        Disable server greeting:
            .greeting on

        Enable server greeting
            .greeting off

        Set the greeting:
            .greeting set

        Clear any personalized greetings
            .greeting clear

        View your greeting
            .greeting view
        """

        if setting == "on":
            await self.db.set_greeting_status(ctx.guild.id, 1)
            await ctx.send("Enabled greeting")

        elif setting == "off":
            await self.db.set_greeting_status(ctx.guild.id, 0)
            await ctx.send("Disbled greeting")

        elif setting == "clear":
            await self.db.clear_greeting(ctx.guild.id)
            await ctx.send("Greeting has been cleared.")

        elif setting == "set":
            await ctx.send("What would you like your greeting to say?")
            msg = await self.bot.wait_for('message', timeout=60,
                                          check=check_author(ctx.author))
            if msg.content == 'cancel':
                return await ctx.send("Cancelling.")

            await self.db.set_greeting(ctx.guild.id, msg.content)
            await ctx.send("Your greeting has been set. It looks like this")
            msg = await on_join_builder(ctx.author, msg.content)
            await ctx.send(embed=msg)

        elif setting == "view":
            greeting = await self.db.get_greeting(ctx.guild.id)
            greeting = await on_join_builder(ctx.author, greeting)
            await ctx.send(embed=greeting)

        else:
            await ctx.send("Valid options are 'on', 'off', or 'set', or "
                           "'view'")

    @commands.command(hidden=True, description="Shuts down the bot",
                      aliases=['po'])
    @commands.is_owner()
    async def halt(self, ctx):
        f"""
        Shuts the bot down.

        Only the owner of the bot may shut the bot down.

        usage: {self.prefix}halt
        """

        shutdown_message = await admin_utils.shutdown_message()
        await admin_utils.write_shutdown_file()

        # Add some dots to clarify that the shortened message is intentional
        await ctx.send(f"{shutdown_message}"+shutdown_message[-1]*4+"....")

        self.bot.logger.log(msg="Bot is shutting down", level=50)
        await client.Client.close(self.bot)

    @halt.error
    async def halt_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("https://http.cat/403.jpg")
        else:
            await ctx.send("Something is wrong with your command.\n"
                           f"Error message: {error}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def leave(self, ctx):
        """Asks the bot to leave the guild."""

        await ctx.send("Please type 'confirm' to have me leave.")

        msg = await self.bot.wait_for('message', timeout=60,
                                      check=check_author(ctx.message.author))

        if msg.content.lower() == "confirm":
            await ctx.guild.leave()

    async def load_cogs(self):
        """
        Handles loading all cogs in for the bot.
        """

        cogs = [cog for cog in os.listdir('cogs')
                if os.path.isfile(f"cogs/{cog}")]

        cogs = [cog.replace(".py", "") for cog in cogs]

        for cog in cogs:
            try:
                print(f"Unloading {cog}")
                self.bot.unload_extension(f"cogs.{cog}")
            except commands.errors.ExtensionNotLoaded:
                print(f"Cog {cog} is already unloaded.")

        for cog in cogs:
            try:
                print(f"Loading {cog}...")
                self.bot.load_extension(f"cogs.{cog}")
                print(f"Loaded {cog.split('.')[-1]}")

            except ModuleNotFoundError:
                msg = f"Could not find {cog}. Does it exist?"
                admin_utils.log_and_print(self.bot, msg)

            except OSError as lib_error:
                msg = "Warning: Opus may not be installed"

                admin_utils.log_and_print(self.bot, msg)
                admin_utils.log_and_print(self.bot, lib_error)

            except commands.errors.ExtensionAlreadyLoaded:
                msg = f"The cog {cog} is already loaded.\n" \
                      "Skipping the load process for this cog."

                admin_utils.log_and_print(self.bot, msg)

            except SyntaxError as e:
                print(f"The cog {cog} has a syntax error.")
                traceback.print_tb(e.__traceback__)

    @commands.command(hidden=True, description="Change log level")
    @commands.is_owner()
    async def logging(self, ctx, log_level):
        f"""
        Changes the log level for the bot. Several log levels are available.
            CRITICAL
            ERROR
            WARNING
            INFO
            DEBUG

        usage:
            set the logging level to debug:
            {self.prefix}logging debug
        """
        logging_levels = ["critical", "error", "warning", "info", "debug"]
        log_level = log_level.lower()

        if log_level in logging_levels:
            log_level = log_level.upper()
            await admin_utils.change_log_level(self.bot, log_level)
            await ctx.send(f"Log level changed to {log_level}")
        else:
            await ctx.send("Invalid logging level specified.")

    @commands.command(hidden=True, description="Show guild member activity.")
    @commands.has_permissions(administrator=True)
    async def member_activity(self, ctx):
        f"""
        Gets a list of all members in the discord guild (discord server) and
        then returns the date they joined.

        {self.prefix}member_activity
        """

        guild = ctx.guild
        members = guild.members

        for i in members:
            await ctx.send(f"```css\n"
                           f"{i.name}\n"
                           f"Joined on: {i.joined_at}```")

    @commands.command(hidden=True,
                      description="Reboots the bot")
    @commands.is_owner()
    async def reboot(self, ctx):
        f"""
        Reboots the bot
        Requires administrator permissions.

        usage: {self.prefix}reboot
        """

        await ctx.send("rebooting....")
        await client.Client.close(self.bot)

    @commands.command(hidden=True,
                      description="Reloads bot cogs")
    @commands.is_owner()
    async def reload(self, ctx, pull=None):
        """
        Reloads all bot cogs.

        This allows updates to be performed while the bot is running. Updates
        to files outside of the cogs directory will require a reboot of the
        bot.

        Examples:
            Reload cogs locally
            .reload
        """
        await self.load_cogs()
        await ctx.send("Reloaded")

    @commands.command(hidden=True, description="Rename the bot")
    @commands.has_permissions(manage_nicknames=True)
    async def rename(self, ctx, *new_name):
        f"""
        Rename the bot in discord.

        Note: If the bot has a nickname, this will not change the nickname.

        Examples:
            Rename the bot to fred
            {self.prefix}rename fred
        """

        await ctx.guild.me.edit(nick=" ".join(new_name))
        await ctx.send("Bot's name has been changed.")

    @commands.command(hidden=True, description="Channel message spammer")
    @commands.has_permissions(manage_messages=True)
    async def spam(self, ctx, limit=5):
        f"""
        Spams messges to a channel.

        usage:
            send 200 messages to a channel
                {self.prefix}spam 200
        """

        try:
            limit = int(limit)
        except ValueError:
            await ctx.send("The limit must be an integer")

        if limit > 1000:
            limit = 1000
            return await ctx.send("Using max limit of 1000")

        for i in range(0, limit):
            await ctx.send(f"Message {i}.")
            await sleep(1)

    @spam.error
    async def spam_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You need manage_message permissions.\n"
                           "https://http.cat/403.jpg")
        else:
            self.bot.logger.log(msg=error, level=20)
            await ctx.send("Something is wrong with your command.\n"
                           f"Error message: {error}")


async def setup(bot):
    await bot.add_cog(admin(bot))
