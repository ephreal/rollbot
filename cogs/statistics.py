# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

from datetime import datetime
from discord.ext import commands


class Statistics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="")
    async def uptime(self, ctx):
        """
        See the bot's uptime.

        usage:
            .uptime
        """
        curr_time = datetime.now()
        difference = curr_time - self.bot.boot_time
        days = difference.seconds // 86400
        minutes = (difference.seconds - (days * 86400)) // 60
        message = f"The bot has been up for {days} days, " \
                  f"and {minutes} minutes"

        await ctx.send(message)


def setup(bot):
    bot.add_cog(Statistics(bot))
