# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

from utils import message_builder
from utils.rolling import rolling_utils
from discord.ext import commands


class DnD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="DnD bot roller")
    async def dnd(self, ctx):
        """
        The main DnD handler.

        If no options are passed in, this will return a 1d20 roll.

        Valid options are:
            help
            roll

        For additional help, run .dnd help <command>, for example, to get help
        for the dnd rolling command:
            .dnd help roll
        """

        advantage = False
        disadvantage = False
        modifier = 0

        channel = await rolling_utils.check_roll_channel(ctx, self.bot)

        command = ctx.message.content.lower().split()
        command = command[1:]

        message = ""
        if len(command) < 1:
            roll = await rolling_utils.roll(1, 20)
            message += "You rolled a 20 sided die.\n"\
                       f"Your result was {roll}"
            message = await message_builder.embed_reply(ctx.author, message)
            return await ctx.send(embed=message)

        # Check for advantage or disadvantage
        if "adv" in command:
            command.remove("adv")
            advantage = True

        if "dis" in command:
            command.remove("dis")
            disadvantage = True

        if len(command) > 0 and ("+" in command[0] or "-" in command[0]):
            modifier = command[0]
            command.remove(modifier)
            modifier = int(modifier)

        if advantage and disadvantage:
            advantage = False
            disadvantage = False

        if advantage:
            message += "You rolled 2d20 with advantage.\n"
            roll = await rolling_utils.roll(2, 20)
            message += f"Rolls : {roll}\n"
            roll = max(roll)

        elif disadvantage:
            message += "You rolled 2d20 with disadvantage.\n"
            roll = await rolling_utils.roll(2, 20)
            message += f"Rolls : {roll}\n"
            roll = min(roll)

        else:
            message += "You rolled a d20.\n"
            roll = await rolling_utils.roll(1, 20)
            roll = roll[0]

        message += f"\nModifier : {modifier}\n"
        message += f"Roll : {roll}\n"
        message += f"Final result : {roll + modifier}\n"

        message = await message_builder.embed_reply(ctx.author, message)

        await channel.send(embed=message)

async def setup(bot):
    await bot.add_cog(DnD(bot))
