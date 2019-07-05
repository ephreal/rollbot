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
import discord
from discord.utils import get


class utils():
    def __init__(self, bot):
        self.bot = bot
        self.rolls = {}

        try:
            with open("config/config.json", 'r') as f:
                self.rolling_channels = json.load(f)["rolling_channels"]
        except FileNotFoundError:
            self.rolling_channels = None

    async def check_roll_channel(self, ctx):
        """
        Verifies that bot is allowed to send the output
        of roll commands to this channel.
        """

        # Return the current channel if no rolling channels are defined
        if not self.rolling_channels:
            return ctx.message.channel

        # Allow rolling in DM channels
        if isinstance(ctx.message.channel, discord.DMChannel):
            return ctx.message.channel

        channel = ctx.message.channel.name
        server = ctx.message.guild

        if channel not in self.rolling_channels:
            # PM author if in wrong channel
            await ctx.author.send("Please limit rolling commands to"
                                  "the rolling or bottesting channels.\n"
                                  "The results of your command will be"
                                  "found in the rolling channel")

            await ctx.message.delete()

            channel = get(server.channels, name=self.rolling_channels[0],
                          type=discord.ChannelType.text)

            command = ctx.message.content
            await ctx.send(f"Command was \"{command}\"")
            return channel

        else:
            return ctx.message.channel

    async def add_roll(self, author_id, roll):
        """
        Adds an author id/roll combination to self.rolls to allow rerolling of
        dice at a later time.
        """

        self.rolls[author_id] = roll

    async def last_roll(self, author_id):
        """
        Retrieves the last roll that was rolled by "author_id"
        """

        try:
            return self.rolls[author_id]
        except KeyError:
            return None
