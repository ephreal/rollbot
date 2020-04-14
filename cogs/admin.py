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
from subprocess import Popen, PIPE
from utils import admin_utils


class admin(commands.Cog):
    """
    Available commands
    .halt
    .logging
    .member_activity
    .reboot
    .reload
    .rename
    .spam
    """
    def __init__(self, bot):
        self.bot = bot
        self.analytics = analytics.GuildAnalytics()
        self.prefix = {self.bot.command_prefix}
        admin_utils.setup_logging(bot)

    @commands.command(hidden=True,
                      description="Shuts down the bot",
                      aliases=['po'])
    @commands.is_owner()
    async def halt(self, ctx):
        f"""
        Shuts the bot down.
        Requires administrator permissions to run.

        usage: {self.prefix}po
        """

        shutdown_message = await admin_utils.shutdown_message()
        await admin_utils.write_shutdown_file()
        # Add some dots to clarify that the shortened message is intentional
        await ctx.send(f"{shutdown_message}"+shutdown_message[-1]*4+"....")
        await client.Client.logout(self.bot)

    @halt.error
    async def halt_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You must be an administrator")
        else:
            await ctx.send("Something is wrong with your command.\n"
                           f"Error message: {error}")

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
                print(f"Could not find {cog}. Does it exist?")

            except OSError as lib_error:
                print("Opus is probably not installed")
                print(f"{lib_error}")

            except commands.errors.ExtensionAlreadyLoaded:
                print(f"The cog {cog} is already loaded.\n"
                      "Skipping the load process for this cog.")

            except SyntaxError as e:
                print(f"The cog {cog} has a syntax error.")
                traceback.print_tb(e.__traceback__)

    @commands.command(hidden=True, description="Change log level")
    @commands.is_owner()
    async def logging(self, ctx, log_level):
        """
        Changes the log level for the bot. Several log levels are available.
            CRITICAL
            ERROR
            WARNING
            INFO
            DEBUG

        usage:
            set the logging level to debug:
            .logging debug
        """
        logging_levels = ["critical", "error", "warning", "info", "debug"]
        if log_level.lower() in logging_levels:
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
        Reboots the bot so all files can be reloaded.
        Requires administrator permissions.

        usage: {self.prefix}reboot
        """

        cmd = Popen(["git", "pull"], stdout=PIPE)
        out, _ = cmd.communicate()
        out = out.decode()
        if "+" in out:
            await ctx.send(f"Updated:\n{out}")

        await ctx.send(f"rebooting....")
        await client.Client.logout(self.bot)

    @commands.command(hidden=True,
                      description="Reloads bot cogs")
    @commands.is_owner()
    async def reload(self, ctx, pull=None):
        """
        Reloads all bot cogs so updates can be performed while the bot is
        running. Reloading can be from local files OR can pull the most
        recent version of the files from the git repository.

        This reloads files locally by default.

        Examples:
            Reload cogs locally
            .reload

            Pull files from github and reload the cogs
            .reload pull
        """

        if pull == "pull":
            cmd = Popen(["git", "pull"], stdout=PIPE)
            out, _ = cmd.communicate()
            await ctx.send(f"Attempted to pull files from github.\n"
                           f"{out.decode()}")

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

    @commands.command(hidden=True,
                      description="Channel message spammer")
    @commands.has_permissions(administrator=True)
    async def spam(self, ctx):
        f"""
        Spams messges to a channel.

        Sometimes you need to test things on a large amount of
        messages. For those times, the spam command will be
        your friend. Instead of having to individually create
        hundreds of messages, why not have a bot do it for you?

        The maximum amount of messages allowed is 1000.

        Requires administrator permissions to run.

        usage:
            send 10 messages to a channel
                {self.prefix}spam or {self.prefix}spam 10

            send 200 messages to a channel
                {self.prefix}spam 200
        """

        command = ctx.message.content.split()
        command = command[1:]

        try:
            if len(command) == 0:
                amount = 10
            else:
                amount = int(command[0])

            if amount > 1000:
                return await ctx.send("I can't spam more than 1000 messages "
                                      "at a time. Please try again.")

            for i in range(0, amount):
                await ctx.send(f"Message {i}.")
                await sleep(1)

        except Exception as e:
            await ctx.send("Invalid input received.")
            await ctx.send(f"Error follows:\n{e}")

    @spam.error
    async def spam_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You must be an administrator to use this command.")
        else:
            await ctx.send("Something is wrong with your command.\n"
                           f"Error message: {error}")

        await ctx.send("Complete")


def setup(bot):
    bot.add_cog(admin(bot))
