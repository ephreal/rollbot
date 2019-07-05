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

from classes.roll_functions import roller
from discord.ext import commands


class vampire_masquerade(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.roller = roller()

    @commands.command(description="Vampire the Masquerade commands")
    async def vm(self, ctx):
        """
        A collection of commands for Vampire the Masquerade.

        Available commands:
            .vm

        Examples:
            roll 2 dice
            .vm 2

        for more help, try running
            .vm help
        """

        result = "```CSS\n"
        result += f"Ran by {ctx.message.author.name}\n"

        cmd = ctx.message.content.split(" ")[1:]

        if len(cmd) > 0:

            try:
                roll = int(cmd[0])
            except Exception:
                roll = 1

            result += f"Rolled {roll} dice\n"

            roll = await self.roller.roll(roll, 10)
            roll.sort()

        else:
            result += "rolling 1 die\n"
            roll = await self.roller.roll(1, 10)

        result += f"Results: {roll}"
        result.replace("[", "")
        result.replace("]", "")
        result += "```"
        return await ctx.send(result)


def setup(bot):
    bot.add_cog(vampire_masquerade(bot))
