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

from asyncio import sleep
from discord.ext import commands


class utils:
	def __init__(self, bot):
		self.bot = bot
		self.timers = []

	@commands.command(pass_context=True,
					  description="Timer/Reminder")
	async def timer(self, ctx):
		"""
		Sets a timer

		timer sets a timer for X minutes/seconds/hours that messages you
		when time is up. This assumes seconds if you do not pass in a 
		length value. The maximum available time you may set a timer for is
		3 hours.

		usage:
			30 second timer: .timer 30 s    or    .timer 30
			10 minute timer: .timer 10 m
			1 hour timer:    .timer 1 h
		"""

		command = ctx.message.content.lower().split()
		command = command[1:]

		valid_intervals = {
							"s" : 1,
							"m" : 60,
							"h" : 3600
						  }
		timer = 1

		try:
			if len(command) == 0:
				return await self.bot.say("How long do you want a timer set for?\n" \
					                      "See '.help timer' for more info.")

			elif len(command) == 1:
				await self.bot.say(f"Assuming {command[0]} seconds.")
				command.append("s")

			if command[1] not in list(valid_intervals.keys()):
				await self.bot.say(f"Unknown time of {command[1]}, assuming seconds...")
				await self.bot.say(f"{command}")
				command[1] = 's'

#			if command[1] == 'm':
#				timer = 60
#			elif command[1] == 'h':
#				timer = 3600

			timer = int(command[0])
			interval = command[1]

			timer *= valid_intervals[interval]

			if timer >= (3600 * 3):
				return await self.bot.say("Max time allowed is 3 hours.")

			await self.bot.say(f"Timer set for {command[0]} {command[1]}")
			
			await sleep(timer)

			await self.bot.send_message(ctx.message.author, "Timer is up!")			

		except Exception as e:
			await self.bot.say("Invalid input received.")
			await self.bot.say(f"Error follows:\n{e}")





def setup(bot):
	bot.add_cog(utils(bot))
