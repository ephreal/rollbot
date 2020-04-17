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
        self.bot.db_handler.init_tables()

    @commands.command(description="Bot uptime")
    async def uptime(self, ctx):
        """
        See the bot's uptime.

        usage:
            .uptime
        """

        await ctx.send(await bot_metrics.uptime_calculation(self.bot))

    @commands.command(description="Command usage", aliases=['cmd'])
    async def commands(self, ctx, command=None):
        """
        View command usage.

        usage:
            .cmd <command>
        """

        if not command:
            usage = await self.bot.db_handler.get_all_usage()
            for reply in await bot_metrics.format_all_usage(usage):
                await ctx.send(embed=reply)
        else:
            usage = await self.bot.db_handler.get_usage(command)
            await ctx.send(f"That command has been used {usage} times")


def setup(bot):
    bot.add_cog(Metrics(bot))
