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

    @commands.command(description="")
    async def uptime(self, ctx):
        """
        See the bot's uptime.

        usage:
            .uptime
        """

        await ctx.send(await bot_metrics.uptime_calculation(self.bot))


def setup(bot):
    bot.add_cog(Metrics(bot))
