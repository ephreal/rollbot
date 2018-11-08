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

from discord.ext import commands
from discord import client

class tests:

	def __init__(self, bot):
		self.bot = bot

	@commands.command(description="Bot connectivity test")
	async def ping(self):
		await self.bot.say("pong!")

	@commands.command(pass_context=True,
		              description="Get server/channel info")
	async def info(self, ctx):
		info = {
				"server"     : ctx.message.server,
				"server_id"  : ctx.message.server.id,
				"channel"    : ctx.message.channel,
				"channel_id" : ctx.message.channel.id,
				"author"     : ctx.message.author,
				"author_id"  : ctx.message.author.id
			   }
		# print(dir(ctx.message.server))

		message = f"""
server: {info['server']}
server id: {info['server_id']}
channel: {info['channel']}
channel id: {info['channel_id']}
author: {info['author']}
author id: {info['author_id']}
"""
		await self.bot.say(message)

	@commands.command()
	async def redirect(self):
		# rolling: 501257611157569556
		# bottesting: 372413873070014464
		# tabletop: 372119891966296066
		
		channel = client.Client.get_channel(self.bot, id='372413873070014464')

		await self.bot.say("Attempting to send message to bot testing channel")
		await self.bot.send_message(channel, "Did I do good?")

	@commands.command()
	async def all_info(self):
		channels = [x.name for x in client.Client.get_all_channels(self.bot)]
		await self.bot.say(channels)

def setup(bot):
	bot.add_cog(tests(bot))