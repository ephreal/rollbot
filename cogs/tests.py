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
from asyncio import sleep
from discord.ext import commands
from discord import client

class tests:

	def __init__(self, bot):
		self.bot = bot

	@commands.command(description="Bot connectivity test")
	async def ping(self):
		"""
		Checks bot availability

		Ping lets you know if the bot can hear and respond
		to you. In usual network fashion, a ping receives
		a pong packet in response.

		usage: .ping
		"""
		await self.bot.say("pong!")

	@commands.command(pass_context=True,
		              description="Gets basic server info")
	async def info(self, ctx):
		"""
		Basic server, channel, and user info

		This is the shortened version of the .all_info command.

		It does not return as much information as .all_info, but
		it dows give you a quick and dirty rundown of server
		info, current channel info, and your user info.

		usage: .info
		"""
		info = {
				"server"     : ctx.message.server,
				"server_id"  : ctx.message.server.id,
				"channel"    : ctx.message.channel,
				"channel_id" : ctx.message.channel.id,
				"author"     : ctx.message.author,
				"author_id"  : ctx.message.author.id
			   }
		# print(dir(ctx.message.server))

		message = f"""```CSS
server:     {info['server']}
server id:  {info['server_id']}
channel:    {info['channel']}
channel id: {info['channel_id']}
author:     {info['author']}
author id:  {info['author_id']}
```
"""
		await self.bot.say(message)


	@commands.command(pass_context = True,
		              description="Get a large amount of useful " \
		                          "server channel/user info")
	async def all_info(self, ctx):
		"""
		Gets server information

		Shows you what channels are currently on the server
		and who your server's members are.

		Note: This command has a built in slowdown in
		returning the user data. This is because there can
		be a lot of information, and the bot WILL be rate
		limited if the slowdown is not enforced.

		usage: .all_info
		"""
		channels = [x.name for x in ctx.message.server.channels]#client.Client.get_all_channels(self.bot)]
		# channels = [{channel : channel.id} for channel in discord.utils.get(channels)]

		users = [member for member in ctx.message.server.members]
		users = [{member.name : [member.id, member.roles]} for member in users]

		for user in users:
			for key in user.keys():
				roles = []
				for role in user[key][1]:
					role = role.name
					if role == "@everyone":
						continue
					roles.append(role)
				user[key][1] = roles


		await self.bot.say(f"```CSS\nchannels:\n\t{channels}```")
		await self.bot.say("users:\n")


		for user in users:
			name = list(user.keys())[0]
			user_id = user[name][0]
			roles = user[name][1]
			message  =  "```CSS\n"
			message += f"Name : {name}\n" \
				       f"\tID: {user_id}\n" \
				       f"\tRoles: {roles}\n```"
			await self.bot.say(message)
			await sleep(1)
		await self.bot.say("All info complete.")

def setup(bot):
	bot.add_cog(tests(bot))
