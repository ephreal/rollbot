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
import random
import aiohttp

from discord.ext import commands
from discord import client


class shadowrun:

	def __init__(self,bot):
		self.bot = bot
		# Maybe I'll put these in an external config file later...
		self.sr_tweaks = {
						   "glitch_more_than_half"          : True,
						   "glitch_fails_extended"          : False,
						   "critical_glitch_fails_extended" : True
						 }
		with open("config/config.json", 'r') as f:
			self.rolling_channels = json.load(f)["rolling_channels"]

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
				.sr r 10

			initiative:
				roll 3 dice, add 8 to the result
				.sr initiative 3 8
				.sr i 3 8

			extended:
				roll an extended test with a dicepool of 20
				and a threshold of 5.
				.sr extended 20 5
				.sr e 20 5

		For more in depth help, please run .sr help <command>

		This command is currently unfinished. More features
		are planned on being added in the future.
		"""

		author = ctx.message.author.name
		author = author.split("#")[0]

		message = f"```Please try again {author}, I'm not sure what to do with that."

		command = ctx.message.content.lower().split()
		command = command[1:]

		if len(command) == 0:
			return await self.bot.say("please run '.help sr' or .sr help for examples.")

		channel = await self.check_channel(ctx)

		available_commands = {
							  "roll"       : self.roll,
		 					  "initiative" : self.roll_initiative,
		 					  "help"       : self.sr_help,
							  "extended"   : self.extended,
							  "quote"	   : self.quote
							 }

		if command[0] in list(available_commands.keys()):
			message = f"```CSS\nRan by {author}\n"
			message += await available_commands[command[0]](command[1:])
		else:
			# Check if the command merely starts with the letter
			# of a known command. It's easy to misspell a
			# command.
			if command[0].startswith("r"):
				message = f"```CSS\nRan by {author}\n"
				message += await available_commands["roll"](command[1:])
			elif command[0].startswith("i"):
				message  = message = f"```CSS\nRan by {author}\n"
				message += await available_commands["initiative"](command[1:])
			elif command[0].startswith("h"):
				message  = f"```CSS\n"
				message += await available_commands["help"](command[1:])
			elif command[0].startswith("e"):
				message  = f"```CSS\nRan by {author}\n"
				message += await available_commands["extended"](command[1:])
			elif command[0].startswith("q"):
				message  = f"```CSS\nRan by {author}\n"
				message += await available_commands["quote"](command[1:])

		message += "```"

		await self.bot.send_message(channel, message)


	async def sr_help(self, command):
		"""
		Additional help for sr commands.

		Added because the current help for sr is getting
		a bit too long. This allows getting info for a
		specific command without having to wade through
		a bunch of extraneous info.
		"""

		if len(command) == 0:
			helptext = """
			Help for sr commands.

			.sr help gives you additional help for all .sr
			commands. Available sr commands are

			help (h)
			extended (e)
			initiative (i)
			roll (r)

			To use it, simply run 
			.sr help <command>

			Examples:
				Get help for the roll command
				.sr help roll
				.sr help r
			"""

		elif command[0].startswith("e"):
			helptext = """
			Shadowrun extended test rolling

			.sr extended allows rolling for extended tests.
			Give it the dice pool to roll with, and the
			threshold to try meet, and it will roll until
			the hits either meet/pass the threshold, or until
			the dice run out.

			If the commands are configured to fail when a
			glitch or critical glitch occur, the extended test
			will fail and let you know that a glitch/critical
			glitch occured.

			Critical glitches fail the exteded test by default.

			Examples:
				run an extended test with a pice pool of 10 and
				a threshold of 5
				.sr extended 10 5
				.sr e 10 5

				Extended test. Dice pool 20, threshold 10
				.sr extended 20 10
				.sr e 20 10
			"""

		elif command[0].startswith("i"):
			helptext = """
			Shadowrun initiative rolling

			.sr initiative allows rolling for initiative and
			automatically add in any modifiers.

			When rolling initiative, the first number is the
			amount of dice to roll (up to 5 per shadowrun
			rules), and the second number is the modifier.

			Like most sr commands, this command can be
			shortened to just "i".

			.sr i <dice> <modifier>

			Examples:
				roll 4 dice, add 10 to the result
				.sr initiative 4 10

				roll 5 dice, add 10 to the result
				.sr i 5 10
			"""

		elif command[0].startswith("r"):
			helptext = """
			Shadowrun dice rolling.

			.sr roll allows you to roll dice using the rules
			for Shadowrun. This includes automatically
			counting hits, misses, and ones. In addition, the
			command accepts various flags to modify how hits,
			misses, ones, and glitches are handles.

			The roll command can be shortened to just "r" for
			convenience.

			Accepted flags: prime, show

			Examples:
				roll 10 dice. Counts hits, checks for glitches.
				.sr roll 10
				.sr r 10

				roll 10 dice, count 4's as a hit (prime runner
					quality)
				.sr roll 10 prime

				roll 10 dice, show the result of all rolls
				.sr roll 10 show

				roll 10 dice, count 4's as hits. Show all rolls.
				.sr roll 10 show prime
				.sr r prime show 10
			"""

		return helptext.replace("\t\t\t", "")


	async def extended(self, commands):
		"""
		Rolls extended tests for shadowrun, checks for
		glitches that may or may not occur, and returns the
		result.

		If glitch_fails_extended is true, a normal glitch
		will cause the extended test to fail. If it is not
		true, a normal glitch will allow the test to finish.
		glitch_fails_extended is off by default.

		If critical_glitch_fails_extended is true, then a
		critical glitch will cause the extended test to fail
		automatically. This is turned on by default.
		"""

		if len(commands) < 2:
			return "Invalid extended test. Please try again.\n" \
			       "See '.sr help extended' for help."

		dice_pool = int(commands[0])
		threshold = int(commands[1])
		rolls = []
		total_hits = 0
		glitch = False

		while total_hits < threshold and dice_pool > 0:
			roll   = await self.multi_roll(dice_pool)
			hits   = await self.get_hits(roll)
			total_hits += hits[0]
			glitch = await self.check_glitch(dice_pool, hits[0], hits[2])
			roll = [
					f"total hits: {total_hits}",
			        f"hits: {hits[0]}",
			        f"rolls: {roll[0:]}"
			        ]

			if glitch:
				if glitch == "critical":
					roll.append("A critical glitch occured!")
				else:
					roll.append("A glitch occured!")

			rolls.append(roll)

			if glitch and self.sr_tweaks["glitch_fails_extended"]:
				break
			elif glitch=="critical" and self.sr_tweaks["critical_glitch_fails_extended"]:
				break


			dice_pool -= 1

			glitch = False

		message = ""
		if total_hits < threshold:
			message = "Extended test failed...\n"

		message += await self.prettify_results(rolls=rolls, roll_type="extended")

		return  message





	async def roll_initiative(self, rolls):
		"""
		Initiative rolling for shadowrun.

		The initiative rolls have the amount of dice first,
		and the amount to add to the roll result second.

		1 +5 means roll one die and add 5 to the result.
		"""

		initiative = 0
		try:
			dice_pool = int(rolls[0])
			to_add = int(rolls[1])

			initiative_rolls = await self.multi_roll(dice_pool)
			for x in initiative_rolls:
				initiative += x

			initiative += to_add

			initiative = await self.prettify_results(rolls=initiative_rolls, hits=initiative, roll_type="initiative")
			return initiative
		except Exception as e:
			return f"Invalid input, exception follows...\n{e}"


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

		message = await self.prettify_results(rolls=rolls, hits=hits, glitch=glitch, roll_type="roll")

		if all_info:
			message += f"Rolls: {rolls}"
		return message


	async def multi_roll(self, amount):
		"""
		returns rolls for a specified amount of dice. All
		rolls are assumed to be six sided dice.
		"""

		rolls = []
		for _ in range(0,amount):
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

		# Rounds down for glitch tests
		if self.sr_tweaks["glitch_more_than_half"]:
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

			# Add in ones variable if needed in the future
			hits, miss, _ = check_rolls(rolls[i])
			threshold -= hits
			if threshold <= 0:
				success = True
				break

			dice -= 1

		return rolls, success


	async def prettify_results(self, rolls=None, hits=None, glitch=None, roll_type=None, success=True):
		"""
		A function to clean up the data and make the results look
		nice before sending the result back to the user.

		Currently knows about one type of roll: roll

		If the roll was a failure (ie: critical glitch on an
		extended test), success is passed in as False.
		"""

		#TODO: Add in check for gremlins 1-4
		message = ""

		if roll_type == "roll":
			if glitch:
				if glitch == "critical":
					message += "A critical glitch occured!\n"
				else:
					message += "A glitch occured!\n"

			message += f"You rolled {len(rolls)} dice.\n"
			message += f"Hits   : {hits[0]}\n"
			message += f"Misses : {hits[1]}\n"
			message += f"Ones   : {hits[2]}\n"

		elif roll_type == "initiative":
			message += f"Initiative score: {hits}\n"
			message += f"Initiative rolls: {rolls}\n"

		elif roll_type == "extended":

			for roll in rolls:
				for i in roll:
					message += f"{i} "
				message += "\n"


		message = message.replace("[", "")
		message = message.replace("]", "")

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
		channel = ctx.message.channel.name

		if not self.rolling_channels:# or self.rolling_channels[0] == "ROLLING_CHANNEL":
			return ctx.message.channel

		if channel not in self.rolling_channels:
			# PM author if in wrong channel
			await self.bot.send_message(author,
				                  "Please limit shadowrun commands to the rolling " \
				                  "or bottesting channels.\nThe results of your " \
				                  "command will be found in the rolling channel")

			# Return the rolling channel
			channel = client.Client.get_channel(self.bot,id=self.rolling_channels[0])
			await self.bot.send_message(channel,
				                        f"Command was \"{ctx.message.content}\"")
			await client.Client.delete_message(self.bot, ctx.message)
			return channel

		else:
			return ctx.message.channel


	async def quote(self, quote_type):

		url = "https://shadowrun.needs.management/api.php?"

		try:
			if not quote_type:
				url += "random=true"
			elif quote_type[0] == "random":
				url += "random=true"
			elif int(quote_type[0]):
				url += f"quote_id={quote_type[0]}"
			else:
				url += "random=true"

		except Exception as e:
			await self.bot.say(e)
			url += "random=true"

		finally:

			async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=True)) as session:
				html = await self.fetch(session, url)
				html = json.loads(html)
				return_string  = f"quote id:     {html['id']}\n"
				return_string += f"written:      {html['time']}\n"
				return_string += f"quote author: {html['author']}\n\n"
				return_string += f"quote title:  {html['title']}\n"
				return_string += f"{html['quote']}"

		return return_string


	async def fetch(self, session, url):
		async with session.get(url) as html:
			return await html.text()


def setup(bot):
	bot.add_cog(shadowrun(bot))
