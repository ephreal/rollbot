# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

from discord.ext import commands
from utils import bot_metrics


class Metrics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db_handler.metrics

    @commands.command(description="Bot uptime")
    async def uptime(self, ctx):
        """
        See the bot's uptime.

        usage:
            .uptime
        """

        await ctx.send(await bot_metrics.uptime_calculation(self.bot))

    @commands.command(description="Command usage", aliases=['cmd'])
    async def cmds(self, ctx, command=None):
        """
        View command usage.

        usage:
            .cmd <command>
        """

        if not command:
            usage = await self.db.get_all_usage()
            for reply in await bot_metrics.format_all_usage(usage):
                await ctx.send(embed=reply)
        else:
            usage = await self.db.get_usage(command)
            await ctx.send(f"That command has been used {usage} times")

    @commands.is_owner()
    @commands.command(description="Clear low use commands")
    async def cmd_clear(self, ctx, uses=1):
        """Clears out low use commands from the database.

        The max amount of uses to clear out by can be passed in.

        Examples
        --------

        Clear out all commands only used once
            .cmd_clear

        clear out all commands used 10 times or less
            .cmd clear 10
        """

        await self.db.clear_usage(uses)
        await ctx.send("Usage has been cleared")

    @classmethod
    async def is_owner(self, ctx):
        return self.bot.appinfo.owner.id == ctx.author.id


async def setup(bot):
    await bot.add_cog(Metrics(bot))
