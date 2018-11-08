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

from discord import client
from discord.ext import commands

class admin:
	def __init__(self,bot):
		self.bot = bot

	@commands.command(pass_context=True)
	async def purge(self, ctx):
		"""
		Usage:
		.purge X

		removes X amount of messages
		from the channel the command
		is ran in.
		"""

		# Disallow anoyone but me from using this
		# currently
		author_id = ctx.message.author.id
		if author_id != '172507494944342017':
			await self.bot.say("That command is restricted " \
				               "to my creator currently.")
			return

		channel = ctx.message.channel
		msgs = []
		limit = ctx.message.content.split()

		if len(limit) >= 2:
			limit = int(limit[1])
		else:
			limit = 10

		async for x in client.Client.logs_from(self.bot, channel, limit=limit):
			msgs.append(x)

		pinned = await client.Client.pins_from(self.bot, channel)
		pinned = [x.id for x in pinned]
		
		# Check msgs for any pinned message and do not
		# delete them.

		for x in msgs:
			if x.id in pinned:
				msgs.remove(x)
				print("removed a message from being purged")
			
		await client.Client.delete_messages(self.bot, msgs)




def setup(bot):
	bot.add_cog(admin(bot))