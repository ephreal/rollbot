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

# This will be a character loading and saving command system.
# The intent is to allow users of the bot to create their DnD character
# through an interactive system with the bot.

from discord.ext import commands
from classes.dice_rolling.base_roll_functions import roller


class DnDChars(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.roller = roller()

    @commands.command()
    async def char(self, ctx):
        """
        Create, modify, and delete DnD characters.

        Examples:
            Create a new character
            .char create

            Delete a character
            .char delete

            Add items to a character
            .char add

            Select a character to be active
            .char select <name>

            See a list of your characters
            .char list

        Functionality that will be added in sometime in the far future:
            download a character
            .char download
        """

        command = ctx.message.content.lower()
        command = command.split(" ")[1:]

        if command[0] == "create":
            await self.create_char(ctx)

    async def create_char(self, ctx):
        """
        Charcater creation handler.

        This is going to be a looooong function... :/

        Uses DnD 5E rules.
        """

        character = {}

        character['char_name'] = await self.name_char(ctx)
        character['stats'] = await self.stat_char(ctx)

    async def name_char(self, ctx):

        def check(m):
            return (m.author == ctx.message.author and
                    m.channel == ctx.message.channel)

        await ctx.send("Welcome to a DnD character creator. What would "
                       "you like to name this character?")

        char_name = await self.bot.wait_for('message', check=check)
        char_name = char_name.content
        await ctx.send(f"Ok, creating {char_name}")
        return char_name

    async def stat_char(self, ctx):
        def check(m):
            return (m.author == ctx.message.author and
                    m.channel == ctx.message.channel)

        await ctx.send("Are you creating this character with\n"
                       "1: Dice rolling\n"
                       "2: Standard stats (15, 14, 13, 12, 10, 8)\n"
                       "3: Point buy (27 points)")
        selecting = True
        while selecting:
            x = await self.bot.wait_for('message', check=check)
            try:
                x = int(x.content)
                if x > 0 and x < 4:
                    selecting = False
                else:
                    await ctx.send("Sorry, that is not a valid choice. Please "
                                   "try again. 1, 2, or 3?")
            except ValueError as e:
                await ctx.send(f"Error: {e}")
                await ctx.send("Sorry, that is not a valid choice. Please "
                               "try again. 1, 2, or 3?")

        if x == 1:
            stats = await self.stats_rolled(ctx)
        elif x == 2:
            stats = await self.stats_standard(ctx)
        elif x == 3:
            stats = await self.stats_point_buy(ctx)

        await ctx.send("I'm sorry, the character creation portion of the bot "
                       "is not completed past this point.")

    async def stats_rolled(self, ctx):
        """
        Handles rolling dice for a stat block.
        """

        stats = await self.roller.roll(24, 6)
        summed_stats = []

        for i in range(0, 24, 4):
            # get 4 of the dice rolls
            stat_range = stats[i:i+4]
            # Arrange the rolls from lowest to highest
            stat_range.sort()
            # Get the three highest rolls and add them together
            stat_range = stat_range[1:]
            stat_range = sum(stat_range)
            summed_stats.append(stat_range)

        summed_stats.sort()
        await ctx.send(f"Your stat block:\n{summed_stats}")
        return summed_stats

    async def stats_standard(self, ctx):
        """
        Returns the standard stats that can be chosen
        at character creation of 15, 14, 13, 12, 10, 8
        """

        stats = [15, 14, 13, 12, 10, 8]
        ctx.send(f"Your stat block: {stats}")
        return stats

    async def stats_point_buy(self, ctx):
        """
        Steps through a point buy system that allows 27 points.
        """

        def check(m):
            return (m.author == ctx.message.author and
                    m.channel == ctx.message.channel)

        await ctx.send("To increase an attribute, use a '+'. To decrease, "
                       "use a '-'. For example, to add to strength, type "
                       "```+str```")

        points = 27
        stats = {'str': 8,
                 'dex': 8,
                 'con': 8,
                 'int': 8,
                 'wis': 8,
                 'cha': 8,
                 }

        keys = stats.keys()

        while points > 0:
            change = await self.bot.wait_for('message', check=check)
            change = change.content.lower()

            if change[1:] in keys:
                if change[0] == "+" and stats[change[1:]] < 15:
                    stats[change[1:]] += 1
                    points -= 1
                elif change[0] == "-" and stats[change[1:]] > 8:
                    stats[change[1:]] -= 1
                    points += 1
                else:
                    await ctx.send("I'm sorry, I can't do that. Please check "
                                   "what you wrote. I can only modify up to "
                                   "15 and as low as 8.")

            await ctx.send(f"points remaining: {points}\n"
                           f"current stats: {stats}")
        return stats


def setup(bot):
    bot.add_cog(DnDChars(bot))
