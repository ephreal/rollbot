# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

from discord.ext import commands
from classes.games import game_handler


class cardgames(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.handlers = {}
    
    @commands.command(description="Plays blackjack with you")
    def blackjack(self, ctx):
        """
        Plays a game of blackjack with the person who ran the command.

        usage:

        .blackjack
        """
        return await ctx.send("Zorp class printer brah!")



async def setup(bot):
    await bot.add_cog(cardgames(bot))
