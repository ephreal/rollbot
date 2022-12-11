# -*- coding: utf-8 -*-

"""
Copyright (c) 2020 Ephreal under the MIT License.
To view the license and requirements when distributing this software, please
view the license at https://github.com/ephreal/catapi/LICENSE.
"""


from discord.ext import commands
from utils.rpg.shadowrun3e.handler import SR3CharacterHandler
from utils.rpg.shadowrun3e.character import SR3Character


class Character(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        mock_user = "tests/mock/sr3_character.json"
        self.character = SR3Character.from_json_file(SR3Character, mock_user)
        self.handler = SR3CharacterHandler(self.character)

    @commands.command(aliases=['c', 'char'])
    async def character(self, ctx):
        try:
            command = ctx.message.content.split()[1:]
            parsed = await self.handler.handle_args(command)
            await ctx.send(parsed)
        except SystemExit:
            pass


async def setup(bot):
    await bot.add_cog(Character(bot))
