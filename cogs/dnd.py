# -*- coding: utf-8 -*-

"""
Copyright 2018-2019 Ephreal

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from classes.dice_rolling.base_roll_functions import roller
from utils import rolling_utils

from discord.ext import commands


class dnd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.roller = roller()

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

        message = "```"
        if len(command) < 1:
            roll = await self.roller.roll(1, 20)
            message += "You rolled a 20 sided die.\n"\
                       f"Your result was {roll}"
            return await ctx.send(message + "```")

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
            roll = await self.roller.roll(2, 20)
            message += f"Rolls : {roll}\n"
            roll = max(roll)

        elif disadvantage:
            message += "You rolled 2d20 with disadvantage.\n"
            roll = await self.roller.roll(2, 20)
            message += f"Rolls : {roll}\n"
            roll = min(roll)

        else:
            message += "You rolled a d20.\n"
            roll = await self.roller.roll(1, 20)
            roll = roll[0]

        message += f"\nModifier : {modifier}\n"
        message += f"Roll : {roll}\n"
        message += f"Final result : {roll + modifier}\n"

        # else:
        #     message += "Please try again. I'm not sure what to do with that."

        message += "```"

        await channel.send(message)


if __name__ == "__main__":
    # Do testing functions here
    # none are made yet....
    pass

else:
    def setup(bot):
        bot.add_cog(dnd(bot))
