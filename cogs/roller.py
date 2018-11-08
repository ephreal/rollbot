import discord
from discord import client
from discord.ext import commands
import random


class roller:
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True)
	async def roll(self, ctx):

		# Check to make sure the bot isn't
		# replying to any bots.

		if ctx.message.author.bot:
			return

		# Channel checks. Rolling is
		# restricted to a few channels
		# on my discord server.
		# Comment out if not desired.
		channel = await self.check_channel(ctx)

		content = ctx.message.content.split()
		content = content[1:]
		
		if len(content) >= 2:
			rolls = await self.multi_roll(int(content[0]), int(content[1]))
		elif len(content) == 1:
			rolls = await self.multi_roll(int(content[0]), 6)
		else:
			# return 1d6 roll
			rolls = await self.multi_roll(1,6)

		await self.bot.send_message(channel, rolls)


	async def single_roll(self, sides):
		return random.randint(1,sides)


	async def multi_roll(self, dice_pool=1, sides=6):
		return [await self.single_roll(sides) for i in range(0,dice_pool)]


	# Info checking functions below
	async def check_channel(self, ctx):
		"""
		Verifies that bot is allowed to send the output
		of roll commands to this channel.
		"""

		# Channels allowed to roll in
		bot_channels = [
						"501257611157569556",
						"372413873070014464"
					   ]

		author = ctx.message.author
		channel = ctx.message.channel.id

		if channel not in bot_channels:
			# PM author if in wrong channel
			await self.bot.send_message(author,
				                  "Please limit roll commands to the rolling " \
				                  "or bottesting channels.\nThe results of " \
				                  "your roll will be found in rolling.")

			# Return the rolling channel
			channel = client.Client.get_channel(self.bot,id=bot_channels[0])
			await self.bot.send_message(channel,
				                        f"Command was \"{ctx.message.content}\"")
			await client.Client.delete_message(self.bot, ctx.message)
			return channel

		else:
			return ctx.message.channel




def setup(bot):
	bot.add_cog(roller(bot))