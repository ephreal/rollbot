# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

from discord.ext import commands
from classes.dice_rolling.base_roll_functions import roller as rl
from utils import rolling_utils

import sys


class roller(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dice_roller = rl()

    @commands.command(pass_context=True)
    async def roll(self, ctx, *rolls):
        """
        A general purpose rolling command.

        Roll will roll XdY dice, where X is the amount of dice,
        and Y is the amount of dice sides. The maximum amount of
        dice that can be rolled at any time is 100.

        usage:
            roll one 6 sided die
                .roll
                .roll 1d6

            roll ten 6 sided die
                .roll 10d6

            roll fifteen 20-sided die
                .roll 15d6

        If you are looking to roll dice for shadowrum, check the
        help for the "sr" command.

        .help sr

        If you are looking to roll with DnD rules, check the help for the
        "dnd" command.

            .help dnd

        """

        channel = await rolling_utils.check_roll_channel(ctx, self.bot)

        message = f"```CSS\nRan by {ctx.author.name}\n"

        try:

            if len(rolls) == 0:
                # return 1d6 roll
                dice_pool = 1
                sides = 6
                rolls = await self.dice_roller.roll(dice_pool, sides)
                rolls = str(rolls)
                rolls = rolls.replace("[", "")
                rolls = rolls.replace("]", "")
                message += f"You rolled {dice_pool}D{sides}\n" \
                           f"{rolls}\n"

            else:
                # different or multiple rolls ahead
                rolls = await self.multiple_rolls(rolls)
                message += await self.format_rolls(rolls)

            message += "```"

            await channel.send(message)

        except Exception as e:
            await channel.send("Incorrect input. Run .help roll if you need "
                               "help.")
            print(f"Error message: {e}\n"
                  f"line: {sys.exc_info()[-1].tb_lineno}")

    async def multiple_rolls(self, roll_types):
        """
        Handles the rolling of anything more complex than a 1d6.

        roll_types: (string)
            -> {roll_type: [int]}
        """

        # Initialize the rolls dictionary
        rolls = {roll: [] for roll in roll_types}
        for roll in roll_types:
            dice, sides = roll.lower().split("d")
            dice = int(dice)
            sides = int(sides)
            rolls[roll].extend(await self.dice_roller.roll(dice, sides))

        return rolls

    async def format_rolls(self, rolls):
        """
        Formats the output from multiple_rolls.

        rolls: {roll: [int]}
            -> formatted_rolls: string
        """

        formatted_rolls = ""
        roll_keys = list(rolls.keys())
        roll_keys.sort()
        for i in roll_keys:
            total = [int(y) for y in rolls[i]]
            formatted_rolls += f"{i}:    total: {sum(total)}\n    " \
                               f"    Rolls: {rolls[i]}\n\n"
        return formatted_rolls


def setup(bot):
    bot.add_cog(roller(bot))
