# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

from utils.rolling import rolling_utils
from discord.ext import commands


class vampire_masquerade(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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

            roll = await rolling_utils.roll(roll, 10)
            roll.sort()

        else:
            result += "rolling 1 die\n"
            roll = await rolling_utils.roll(1, 10)

        result += f"Results: {roll}"
        result.replace("[", "")
        result.replace("]", "")
        result += "```"
        return await ctx.send(result)


def setup(bot):
    bot.add_cog(vampire_masquerade(bot))
