# -*- coding: utf-8 -*-

"""
Copyright (c) 2020 Ephreal under the MIT License.
To view the license and requirements when distributing this software, please
view the license at https://github.com/ephreal/catapi/LICENSE.
"""


from discord.ext import commands


class Character(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['c', 'char'])
    async def character(self, ctx):
        await ctx.send("This command is not ready for use")


def setup(bot):
    bot.add_cog(Character(bot))
