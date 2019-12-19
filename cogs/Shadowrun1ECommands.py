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


from classes.context_handlers import shadowrun_handler as sh
from discord.ext import commands


class Shadowrun1Commands(commands.Cog):
    """
    Shadowrun 1st edition commands.
    """

    def __init__(self, bot):

        self.bot = bot
        self.handler = sh.Shadowrun1Handler()

    @commands.command()
    async def sr1(self, ctx, command, *args):
        """
        Handles all shadowrun 1E commands. Valid commands are:

        .sr1 roll
        .sr1 initiative
        """

        author = ctx.author.name
        message = f"```CSS\nRan by {author}\n"

        dice_pool, modifier = await self.check_command(args)

        if command.startswith("r"):
            message += await self.roll(dice_pool, modifier)

        elif command.startswith("i"):
            message += await self.roll_initiative(dice_pool, modifier)

        message += "```"
        return await ctx.send(message)

    async def check_command(self, args):
        """
        Verifies that a threshold either exists or does not exist
        list[str]

            -> list[int]
        """

        dice_pool = int(args[0])
        modifier = 0
        if len(args) > 1:
            modifier = int(args[1])

        return dice_pool, modifier

    async def roll(self, dice_pool, threshold):
        """
        Handles rolling sr1e style.

        dice_pool: int
        threshold: int

            -> formatted_roll: str
        """

        roll = await self.handler.roll(dice_pool)

        if threshold:
            checked = await self.handler.check_roll(roll, threshold)
            formatted = await self.handler.format_roll(roll, checked)
        else:
            formatted = await self.handler.format_unchecked_roll(roll)

        return formatted

    async def roll_initiative(self, dice_pool, reaction):
        """
        Roll initiative.

        dice_pool: list[int]
        reaction: int

            -> formatted_initiative: str
        """

        roll, initiative = await self.handler.roll_initiative(dice_pool,
                                                              reaction)
        return await self.handler.format_initiative(initiative, roll)


def setup(bot):
    bot.add_cog(Shadowrun1Commands(bot))
