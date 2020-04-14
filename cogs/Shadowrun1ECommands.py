# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""


from utils.handlers import shadowrun_handler as sh
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
