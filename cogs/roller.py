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

from discord import client
from discord.ext import commands
from classes.roll_functions import roller as rl


class roller:
	def __init__(self, bot):
		self.bot = bot
		# Channels the bot is allowed to run roll commands in.
		# Change these in config.json to channels of your choice.
		with open("config/config.json", 'r') as f:
			self.rolling_channels = json.load(f)["rolling_channels"]
		self.dice_roller = rl()

	@commands.command(pass_context=True)
	async def roll(self, ctx, roll):
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

		"""

		# Check to make sure the bot isn't replying to any bots.

		if ctx.message.author.bot:
			return

		# Channel checks. Rolling is restricted to a few channels
		# on my discord server.
		# Comment out if not desired.
		channel = await self.check_channel(ctx)

		try:

			if len(roll) == 0:
				# return 1d6 roll
				rolls = await self.dice_roller.multi_roll(1,6)

			elif len(roll) >= 2:
				roll = roll.split("d")
				dice_pool = int(roll[0])
				sides = int(roll[1])
				rolls = await self.dice_roller.multi_roll(dice_pool, sides)

			await self.bot.send_message(channel, rolls)

		except Exception as e:
			await self.bot.send_message(channel, "Incorrect input. Run .help roll "\
				                                 "if you need help.")
			await self.bot.send_message(channel, f"Error message: {e}")

	# Info checking functions below
	async def check_channel(self, ctx):
		"""
		Verifies that bot is allowed to send the output
		of roll commands to this channel.
		"""

		author = ctx.message.author
		channel = ctx.message.channel.name

		if not self.rolling_channels:# or self.rolling_channels[0] == "ROLLING_CHANNEL":
			return ctx.message.channel

		if channel not in self.rolling_channels:
			# PM author if in wrong channel
			await self.bot.send_message(author,
				                  "Please limit roll commands to the rolling " \
				                  "or bottesting channels.\nThe results of your " \
				                  "roll will be found in the rolling channel")

			# Return the rolling channel
			channel = client.Client.get_channel(self.bot,id=self.rolling_channels[0])
			await self.bot.send_message(channel,
				                        f"Command was \"{ctx.message.content}\"")
			await client.Client.delete_message(self.bot, ctx.message)
			return channel

		else:
			return ctx.message.channel


def setup(bot):
	bot.add_cog(roller(bot))