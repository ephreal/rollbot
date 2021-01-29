# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

from discord.ext import commands
from utils.verification import process_host_commands


class HostCommands(commands.Cog):
    """
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(hidden=True)
    async def sc(self, ctx, *cmd):
        """
        Lets the owner of the bot run a limited subset of commands on the
        server.

        Valid commands are
        df
        free
        uptime
        """

        return await ctx.send(await process_host_commands(cmd))


def setup(bot):
    bot.add_cog(HostCommands(bot))
