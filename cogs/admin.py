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