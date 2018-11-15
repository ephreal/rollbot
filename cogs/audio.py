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
import youtube_dl

from asyncio import sleep
from discord.ext import commands
from discord import client

if not discord.opus.is_loaded():
	discord.opus.load_opus("opus")

class musicPlayer():
	def __init__(self, bot):
		self.bot = bot



	@commands.command(pass_context=True,
		              description="Plays sound from youtube")
	async def play(self,ctx,url=None):
		"""
		Has the bot play music from youtube.

		If no arguments are passed it, it will randomly
		select somthing from the sound list in config.

		usage:
			Play a random sound/song
			.play

			Play a specific video
			.play https://www.youtube.com/watch?v=dQw4w9WgXcQ

		"""

		await client.Client.delete_message(self.bot, ctx.message)

		try:
			vc = await self.bot.join_voice_channel(ctx.message.author.voice_channel)
			player = await vc.create_ytdl_player(url)
			player.start()

		except Exception as e:
			await self.bot.say(f"An error has occured. Message follows....\n{e}")
			await vc.disconnect()


def setup(bot):
	bot.add_cog(musicPlayer(bot))