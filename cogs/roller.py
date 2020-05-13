# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

from discord.ext import commands
from utils import message_builder
from utils.rolling import rolling_utils
from utils.rolling import handlers


class roller(commands.Cog):
    def __init__(self, bot):
        self.handler = handlers.BaseRollHandler()
        self.bot = bot

    @commands.command(pass_context=True)
    async def roll(self, ctx, *roll_args):
        """Rolls dice

        Rolls XdY dice.

        By default, the dice roller rolls dice with the currently set game
        mode. This can be changed with the ".set" command, or by passing in
        the "-g" parameter.

        roll 10, six-sided dice
            .roll 10d6

        Add 5 to 10, six sided dice
            .roll 10d6 -m 5

        Give a note specifying what the note is for
            .roll 1d6 -n This is a test roll
        """

        channel = await rolling_utils.check_roll_channel(ctx, self.bot)

        roll = await self.handler.roll(roll_args)
        message = await roll.format()
        message = await message_builder.embed_reply(ctx.author, message)

        await channel.send(embed=message)


def setup(bot):
    bot.add_cog(roller(bot))
