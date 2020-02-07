# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

import discord
import os
# import youtube_dl
from asyncio import sleep
from discord.ext import commands


from utils.structures import Queue
from classes.music_player import MusicPlayer


class musicPlayer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.players = {}
        # Both voice_clients and music_queues will be removed when the music
        # player is completed.
        self.voice_clients = {}
        self.music_queues = {}

    async def initialize_voice(self, ctx):
        """
        joins the bot to the voice channel the author is in.
        """
        join = "audio/bot_sounds/start_click.mp3"

        channel = ctx.author.voice.channel
        if not channel:
            return await ctx.send("You must be in a voice channel to do that")

        vc = await channel.connect()
        self.voice_clients[ctx.guild.id] = vc
        self.music_queues[ctx.guild.id] = Queue(10)
        self.players[ctx.guild.id] = MusicPlayer(voice_client=vc)

        # I have to play SOMETHING otherwise the bot refuses to play anything
        # later on (is_playing() always returns True)
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(join))
        vc.play(source)
        await sleep(2)
        return vc

    @commands.command()
    async def summon(self, ctx):
        """
        Summons the bot to your voice channel
        """

        channel = ctx.author.voice.channel
        if not channel:
            return await ctx.send("Join a voice channel first.")

        if not self.players[ctx.guild.id]:
            return await self.initialize_voice(channel)

        vc = self.players[ctx.guild.id].voice_client
        await vc.move_to(channel)

    @commands.command()
    async def clear(self, ctx):
        """
        Clears the music queue.
        """

        await self.players[ctx.guild.id].clear()

    @commands.command()
    async def disconnect(self, ctx):
        """
        Disconnects the bot from the voice channel.
        """
        del(self.players[ctx.guild.id])
        await ctx.voice_client.disconnect()

    @commands.command()
    async def stop(self, ctx):
        """
        Stops the bot from playing audio
        """
        player = self.players[ctx.guild.id]
        await player.stop()
        await ctx.send("Stopped voice client")

    @commands.command()
    async def pause(self, ctx):
        """
        Pauses the voice client from playing
        """

        player = self.players[ctx.guild.id]
        await player.pause()
        await ctx.send("Song paused...")

    @commands.command()
    async def play(self, ctx, song=None):
        """
        Searches local audio and plays the song (if found)
        """

        try:
            vc = self.players[ctx.guild.id].voice_client
        except KeyError:
            vc = await self.initialize_voice(ctx)

        if not vc:
            return

        if song is not None:
            if not await self.players[ctx.guild.id].enqueue(song):
                return await ctx.send("The music queue is full.")
            return await ctx.send("Your song has been queue for playback.")

        if not vc.is_playing():
            await self.play_song(ctx)

    async def play_song(self, ctx):
        """
        Plays a song in the queue, whether it be mp3, m4a, or otherwise.
        """

        player = self.players[ctx.guild.id]
        await player.play()

    @commands.command()
    async def resume(self, ctx):
        """
        Resumes playing the paused song.
        """

        player = self.players[ctx.guild.id]
        await player.resume()

    @commands.command()
    async def songs(self, ctx, *path):
        """
        Lists available songs.
        """
        player = self.players[ctx.guild.id]
        path = " ".join(path)
        await ctx.send(await player.available_songs(path))

    @commands.command()
    async def state(self, ctx):
        vc = self.players[ctx.guild.id].voice_client
        queue = self.players[ctx.guild.id].music_queue
        message = f"```css\nmusic queue: {queue.items}\n" \
                  f"up next: {await queue.peek()}\n" \
                  f"playing state: {vc.is_playing()}\n" \
                  "```"
        return await ctx.send(message)


def setup(bot):
    bot.add_cog(musicPlayer(bot))
