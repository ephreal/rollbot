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