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

import json
# import aiohttp

from classes.roll_functions import roller
from classes.bot_utils import utils

from discord.ext import commands
# from discord import client


class dnd:
    def __init__(self, bot):
        self.bot = bot
        self.roller = roller()
        self.utils = utils(self.bot)

        with open("config/config.json", 'r') as f:
            self.rolling_channels = json.load(f)["rolling_channels"]

    @commands.command(pass_context=True,
                      description="DnD bot roller")
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

        channel = await self.utils.check_channel(ctx, self.rolling_channels)

        command = ctx.message.content.lower().split()
        command = command[1:]

        if len(command) < 1:
            roll = await self.roller.single_roll(20)
            message = "You rolled a 20 sided die.\n"\
                      f"Your result was {roll}"

        elif "+" in command[0] or "-" in command[0]:
            # this is a 1d20 roll with modifiers. Pass this to the rolling
            # function immediately to prevent additional checking.
            message = await self.roll(command)

        else:
            message = "Please try again. I'm not sure what to do with that."

        await self.bot.send_message(channel, message)

    async def roll(self, roll_command):
        """
        Checks the roll command for modifiers and any additional dice
        that need to be rolled.

        This function assumes a 20 sided die unless told otherwise.
        """

        message = []

        try:

            if "+" in roll_command[0] or "-" in roll_command[0]:
                message.append("You rolled a 20 sided die.")
                message.append(f"\nModifier : {roll_command[0]}")

                roll = await self.roller.single_roll(20)
                modified_roll = roll + int(roll_command[0])

                message.append(f"Dice roll : {roll}")
                message.append(f"Modified roll : {modified_roll}")

            else:
                message.append("I'm sorry, I don't know what to do with that.")
        except TypeError:
            message = ["There is something wrong with your command."]

        return "\n".join(message)


if __name__ == "__main__":
    # Do testing functions here
    # none are made yet....
    pass

else:
    def setup(bot):
        bot.add_cog(dnd(bot))
