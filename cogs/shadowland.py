# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""


from discord.ext import commands
from utils import message_builder


class shadowland(commands.Cog):
    """
    Commands provided by shadowland:
        about:
            Returns an embed with information about the bot
        quote:
            Gets and returns quotes
        timer:
            Sets a timer for X minutes/seconds/hours
    """
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db_handler.shadowland

    @commands.command()
    async def new_thread(self, ctx, name):
        name = await self.db.create_thread(ctx.guild.id, name)
        await ctx.send(f"Created thread: {name}")


def setup(bot):
    bot.add_cog(shadowland(bot))
