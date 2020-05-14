# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""


from discord import Colour
from discord.ext import commands
from utils.rolling import parsers
from utils.rolling import rolls
from utils.rolling import rolling_utils
from utils import message_builder


class Shadowrun1Commands(commands.Cog):
    """
    Shadowrun 1st edition commands.
    """

    def __init__(self, bot):

        self.bot = bot
        self.parser = parsers.Sr1RollParser()

    @commands.command()
    async def sr1(self, ctx, *roll_args):
        """Rolls dice for SR1E

        Roll args: <dice> <threshold> [-m <modifier>, -n <note>]
        ---------
        dice: how many dice to roll
        threshold: the threshold dice must meet or exceed to be a success
                   Default threshold is 5.
        modifier: A modifier for the threshold difficulty
        note: A note to display with the roll

        Examples
        --------

        roll 4d6 with a threshold of 6
            .sr1 4 6

        roll 4d6, threshold of 5, and a note to explain the roll
            .sr1 4 -n Attempting to bash the ganger's face in
        """

        channel = await rolling_utils.check_roll_channel(ctx, self.bot)

        roll = self.parser.parse_args(roll_args)
        roll = rolls.Sr1Roll(roll)
        await(roll.roll())
        message = await(roll.format())
        if "FAILURE" in message:
            message = await message_builder.embed_reply(ctx.author, message,
                                                        Colour.red())
        else:
            message = await message_builder.embed_reply(ctx.author, message)
        await channel.send(embed=message)


def setup(bot):
    bot.add_cog(Shadowrun1Commands(bot))
