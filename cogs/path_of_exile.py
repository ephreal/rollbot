# -*- coding: utf-8 -*-

"""
Copyright 2018 Ephreal

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

from discord.ext import commands
from classes.roll_functions import roller as rl
from classes.bot_utils import utils


class poe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dice_roller = rl()
        self.utils = utils(self.bot)
        self.rolls = {}

    @commands.command(pass_context=True)
    async def lab(self, ctx, amt: int):
        """
        A specific rolling command to get amt amount of distinct numbers
        ranging from 1 to 10, inclusive. As you'd expect, the largest number
        allowed is 10.
        """

        # Channel checks. Rolling is restricted to a few channels
        # on my discord server.
        channel = await self.utils.check_roll_channel(ctx)

        try:

            amt = int(amt)

            if amt > 10 or amt < 1:
                return await ctx.send("I'm sorry, going larger than 10 or less"
                                      "than one makes no sense")
            else:
                x = 0
                distinct_rolls = [] if distinct_rolls is None
                while x < amt:
                    roll = await self.dice_roller.roll(1, 10)
                    if roll[0] not in distinct_rolls:
                        distinct_rolls.append(roll[0])
                        x += 1

            distinct_rolls.sort()
            await channel.send(distinct_rolls)

        except Exception as e:
            await channel.send("Incorrect input. Run .help lab if you need "
                               "help.")
            await channel.send(f"Error message: {e}")


def setup(bot):
    bot.add_cog(poe(bot))
