from discord import client

class utils():
	def __init__(self, bot):
		self.bot = bot

	async def check_channel(self, ctx, roll_channels):
			"""
			Verifies that bot is allowed to send the output
			of roll commands to this channel.
			"""

			author = ctx.message.author
			channel = ctx.message.channel.name

			if not roll_channels:# or self.rolling_channels[0] == "ROLLING_CHANNEL":
				return ctx.message.channel

			if channel not in roll_channels:
				# PM author if in wrong channel
				await self.bot.send_message(author,
					                  "Please limit shadowrun commands to the rolling " \
					                  "or bottesting channels.\nThe results of your " \
					                  "command will be found in the rolling channel")

				# Return the rolling channel
				await self.bot.say(dir(ctx.message))
				# channel = client.Client.get_channel(self.bot,id=roll_channels[0])
				# await self.bot.send_message(channel,
				# 	                        f"Command was \"{ctx.message.content}\"")
				# await client.Client.delete_message(self.bot, ctx.message)
				return channel

			else:
				return ctx.message.channel