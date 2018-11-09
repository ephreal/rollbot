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

import discord
from discord import client
from discord.ext import commands
import json

class admin:
	def __init__(self,bot):
		self.bot = bot
		self.admins = []
		self.admin_group = "Admins"

	@commands.command(pass_context=True, hidden=True)
	async def purge(self, ctx):
		"""
		Usage:
		.purge X

		removes X amount of messages from the channel the command is 
		ran in. Currently limited to 100 messages at a time. This
		will default to removing 10 messages at a time.

		Message purging ignores any pinned messages or messages with
		attachments by default. To purge everything, include "all"
		after in your purge command.
		"""

		author_id = ctx.message.author.id

		# Get admins if this is the first time it's been ran
		if not self.admins:
			await self.get_admins(ctx)

		# Only allow admins to run admin commands
		if author_id not in self.admins:
			return await self.bot.say("That command is restricted to admins.")

		channel = ctx.message.channel
		msgs = []
		limit = ctx.message.content.split()

		if limit[1] == "all":
			limit = 1000
		elif len(limit) >= 2:
			limit = int(limit[1])
		else:
			limit = 10

		async for x in client.Client.logs_from(self.bot, channel, limit=limit):
			msgs.append(x)

		if not "all" in ctx.message.content:

			# check for pinned messages
			to_keep = await client.Client.pins_from(self.bot, channel)
			to_keep = [x.id for x in to_keep]

			
			# Check msgs for any to_keep messages or messages
			# with attachments and do not delete them.

			for x in msgs:
				if x.id in to_keep:
					msgs.remove(x)

				elif x.attachments:
					msgs.remove(x)


		# delete messages in groups of 100 at a time
		while msgs:
			await client.Client.delete_messages(self.bot, msgs[0:100])
			msgs = msgs[100:]



	@commands.command(hidden=True, pass_context=True)
	async def stop(self,ctx):
		
		author_id = ctx.message.author.id

		if not self.admins:
			await self.get_admins(ctx)

		if author_id not in self.admins:
			return await self.bot.say("Only admins may stop me.")

		await self.bot.say("Shutting d....")
		# await client.Client.close(self.bot)
		await client.Client.logout(self.bot)


	@commands.command(hidden=True, pass_context=True)
	async def refresh_admins(self, ctx):
		self.get_admins(ctx)
		await self.bot.send_message(ctx.message.author, "Admin list refreshed")


	async def get_admins(self, ctx):
		role = discord.utils.get(ctx.message.server.roles, name=self.admin_group)
		for member in ctx.message.server.members:
			if role in member.roles:
				self.admins.append(member.id)

		if len(self.admins) == 0:
			message = f"No admins found. Do you have an \"{self.admin_group}\" group with users?\n" \
			          "(Note: Group name is case sensitive)"

			await self.bot.send_message(ctx.message.channel, message)




def setup(bot):
	bot.add_cog(admin(bot))