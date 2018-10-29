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

import random

from discord.ext import commands


class shadowrun:

	def __init__(self,bot):
		self.bot = bot
		# Maybe I'll put these in an external config file later...
		self.sr_tweaks = {
						   "glitch_more_than_half"          : True,
						   "glitch_fails_extended"          : False,
						   "critical_glitch_fails_extended" : False
						 }

		self.rolling_channels = [
			                     "501257611157569556",
			                     "372413873070014464"
			                    ]

	@commands.command(pass_context=True,
					  description="Shadowrun dice roller")
	async def sr(self, ctx):
		"""
		Shadowrun specific dice rolling.

		The sr command is used for anything related to
		shadowrun. It has three subcommands: roll,
		initiative, and extended. Roll is used for general
		dice rolling, initiative is used to get initiative
		score, and extended is used to roll an extended
		test.

		examples:
			roll:
				roll 10 dice
				.sr roll 10

				roll 10 dice (count 4's as hits)
				.sr roll 10 prime

				roll 10 dice, show rolls
				.sr roll 10 show



		This function is currently unfinished. More features
		are planned on being added in the future.
		"""

		author = ctx.message.author.name
		author = author.split("#")[0]

		message = f"```Please try again {author}, I'm not sure what to do with that.```"

		command = ctx.message.content.lower().split()
		command = command[1:]

		if len(command) == 0:
			return await self.bot.say("please run '.help sr' for examples.")

		channel = await self.check_channel(ctx)

		available_commands = {
							  "roll"       : self.roll#,
		 					  # "initiative" : self.initiative,
							  # "extended"   : self.extended
							 }

		if command[0] in list(available_commands.keys()):
			message = f"```CSS\n@{author}\n"
			message += await available_commands[command[0]](command[1:])
			message += "```"
		else:
			# Check if the command merely starts with the letter
			# of a known command. It's easy to misspell a
			# command.
			if command[0].startswith("r"):
				message = f"```CSS\n@{author}\n"
				message += await available_commands["roll"](command[1:])
				message += "```"
			# elif command[0].startswith("i"):
			# 	message  = message = f"```\n@{author}\n"
			# 	message += await available_commands["initiative"](command[1:])
			# 	message += "```"
			# elif command[0].startswith("e"):
			# 	message  = f"```\n@{author}\n"
			# 	message += await available_commands["extended"](command[1:])
			# 	message += "```"

		await self.bot.send_message(channel, message)


	async def roll(self, dice_pool):
		"""
		Rolls dice for shadowrun.

		If all_info is passed it, this will try return the
		rolls along with the other data. Bear in mind that
		if you roll a ridiculous number of dice with this
		enabled (ie: 1000), you probably won't get anything
		back due to the 2000 character length limit.
		"""

		# Check if this is to be considered a prime runner
		all_info = False
		prime = False
		if len(dice_pool) > 1:
			if "prime" in dice_pool:
				dice_pool.remove("prime")
				prime = True

			if "show" in dice_pool:
				dice_pool.remove("show")
				all_info = True

		dice_pool = int(dice_pool[0])

		rolls  = await self.multi_roll(dice_pool)

		if prime:
			await self.bot.say("Prime runner.")
			hits = await self.get_hits(rolls, prime=True)
		else:
			hits = await self.get_hits(rolls)

		glitch = await self.check_glitch(dice_pool, hits[0], hits[2])

		message = await self.prettify_results(rolls, hits, glitch, "roll")

		if all_info:
			message += f"Rolls: {rolls}"
		return message


	async def multi_roll(self, amount):
		"""
		returns rolls for a specified amount of dice. All
		rolls are assumed to be six sided dice.
		"""

		rolls = []
		for i in range(0,amount):
			rolls.append(random.randint(1,6))

		return rolls


	async def get_hits(self, rolls, prime=False):
		"""
		Returns a list of [hits, misses, ones] when give a
		list of dice rolls.

		prime determines if the runner is a prime runner. A
		prime runner is allowed to have 4's count as hits.
		"""

		hit = 5
		if prime:
			hit = 4

		hits = 0
		misses = 0
		ones = 0

		for roll in rolls:
			if roll >= hit:
				hits += 1
			elif roll >= 2:
				misses += 1
			else:
				ones += 1

		return [hits, misses, ones]



	async def check_glitch(self, dice_pool, hits, ones):
		"""
		Checks a list of dice rolls to see if the roll has
		glitched or not. Returns either False, True, or
		critical depending on the glitch type.
		"""

		glitch = False

		if self.sr_tweaks["glitch_more_than_half"]:
			# Rounding down for glitches
			if ones > (dice_pool // 2):
				glitch = True

		else:
			if ones >= (dice_pool // 2):
				glitch = True

		if glitch and (hits == 0):
			glitch = "critical"

		return glitch


	async def extended_roller(self, dice, threshold):
		"""
		Given the dice pool and the	limit to try reach, this
		rolls until the required amount of hits has been
		reached.
		"""
		max_rolls = dice
		rolls = []
		success = False

		for i in range(0,max_rolls):
			rolls.append(roller.multi_roll(dice, 6))

			hits, miss, ones = check_rolls(rolls[i])
			threshold -= hits
			if threshold <= 0:
				success = True
				break

			dice -= 1

		return rolls, success


	async def prettify_results(self, rolls, hits, glitch, roll_type, success=True):
		"""
		A function to clean up the data and make the results look
		nice before sending the result back to the user.

		Currently knows about one type of roll: roll

		If the roll was a failure (ie: critical glitch on an
		extended test), success is passed in as False.
		"""

		message = ""

		if roll_type == "roll":
			if glitch:
				if glitch == "critical":
					message += "A critical glitch occured!"
				else:
					message += "A glitch occured!"

			message += f"You rolled {len(rolls)} dice.\n"
			message += f"Hits   : {hits[0]}\n"
			message += f"Misses : {hits[1]}\n"
			message += f"Ones   : {hits[2]}\n"

		return message

	# I need to learn how to access functions from
	# another cog here. I know there HAS to be a
	# way, I just don't know it yet. This would
	# save me from some code reuse.
	async def check_channel(self, ctx):
		"""
		Verifies that bot is allowed to send the output
		of roll commands to this channel.
		"""

		author = ctx.message.author
		channel = ctx.message.channel.id

		if channel not in self.rolling_channels:
			# PM author if in wrong channel
			await self.bot.send_message(author,
				                  "Please limit shadowrun commands to the rolling " \
				                  "or bottesting channels.\nThe results of your " \
				                  "commandd will be found in the rolling channel")

			# Return the rolling channel
			channel = client.Client.get_channel(self.bot,id=self.rolling_channels[0])
			await self.bot.send_message(channel,
				                        f"Command was \"{ctx.message.content}\"")
			await client.Client.delete_message(self.bot, ctx.message)
			return channel

		else:
			return ctx.message.channel


def setup(bot):
	bot.add_cog(shadowrun(bot))
