# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

from discord.ext import commands
from classes.indexer import Indexer
from classes.music_player import MusicPlayer
from classes.searcher import IndexSearch

import os


class musicPlayer(commands.Cog):
    """
    Commands provided by this module
    .clear
    .disconnect
    .index
    .next
    .pause
    .play
    .queue
    .resume
    .search
    .stop
    .summon
    """
    def __init__(self, bot):
        self.bot = bot
        self.indexer = Indexer()
        self.searcher = IndexSearch()

    def check(self, author):
        """
        Checks to see if the author of a message is the same as the author
        passed in.
        """

        def check_message(message):
            return message.author == author
        return check_message

    @commands.command(description="Clear music queue")
    async def clear(self, ctx):
        """
        Clears the music queue.
        usage:
            .clear
        """

        await self.bot.players[ctx.guild.id].clear()

    @commands.command(description="Disconnect from voice")
    async def disconnect(self, ctx):
        """
        Disconnects the bot from the voice channel.

        usage:
            .disconnect
        """
        del(self.bot.players[ctx.guild.id])
        await ctx.voice_client.disconnect()

    @commands.command(description="Indexes songs")
    async def index(self, ctx):
        """
        Builds the song index.

        usage:
            .index
        """

        self.indexer.update_index()
        await ctx.send("Indexing complete!")

    async def initialize_voice(self, ctx):
        """
        joins the bot to the voice channel the author is in.
        """

        channel = ctx.author.voice.channel
        if not channel:
            return await ctx.send("You must be in a voice channel to do that")

        vc = await channel.connect()
        self.bot.players[ctx.guild.id] = MusicPlayer(voice_client=vc)

        return vc

    @commands.command(description="Play next song")
    async def next(self, ctx):
        """
        Advances the player to the next song in the queue.

        usage:
            .next
        """
        player = self.bot.players[ctx.guild.id]
        await player.next()

    @commands.command(description="Pause music")
    async def pause(self, ctx):
        """
        Pauses the voice client from playing

        usage:
            .pause
        """

        player = self.bot.players[ctx.guild.id]
        await player.pause()
        await ctx.send("Song paused...")

    @commands.command(description="Play music")
    async def play(self, ctx, *keywords):
        """
        Search the song database and immediately queue up or play a song.

        examples:
            Play the song "gravity".
                .play gravity
        """

        try:
            vc = self.bot.players[ctx.guild.id].voice_client
        except KeyError:
            vc = await self.initialize_voice(ctx)

        if not vc:
            return

        if not keywords:
            # Assume player is paused and try resume
            player = self.bot.players[ctx.guild.id]
            return await player.play()

        results = await self.search_index(ctx, keywords)
        if results is None:
            return

        results = results
        await self.play_from_results(ctx, results)

    async def play_from_results(self, ctx, results):
        """
        Queues up songs in results to play.
        """

        queued = False
        if len(results) > 1:
            # The user must choose a song.
            message = f"```css\n{ctx.author.name}, choose one or more song " \
                      f"numbers for playback"

            counter = 1
            for i in results:
                message += f"\n{counter}: {i.name}"
                counter += 1
            message += "```"

            await ctx.send(message)

            msg = await self.bot.wait_for('message', timeout=60,
                                          check=self.check(ctx.message.author))
            choice = msg.content

            try:
                choice = [int(i)-1 for i in choice.split(" ")]
            except ValueError:
                return await ctx.send("That seems to be an invalid choice.")
        else:
            choice = [0]

        choice = [results[i] for i in choice]
        for i in choice:
            if await self.bot.players[ctx.guild.id].enqueue(i.path):
                queued = True
            else:
                await ctx.send("The music queue is full, please try later.")
        if queued:
            if len(choice) > 1:
                await ctx.send("Your songs were queued.")
            else:
                await ctx.send("Your song has been queued.")

    async def play_song(self, ctx):
        """
        Plays a song in the queue, whether it be mp3, m4a, or otherwise.
        """

        player = self.bot.players[ctx.guild.id]
        await player.play()

    @commands.command(description="View music queue")
    async def queue(self, ctx):
        """
        Displays the music queue to see what songs are up next, what is
        currently playing, etc.

        usage:
            .queue
        """
        player = self.bot.players[ctx.guild.id]
        vc = player.voice_client
        queue = self.bot.players[ctx.guild.id].music_queue

        up_next = await queue.peek()
        if up_next:
            up_next = os.path.basename(up_next)
        message = f"```css\nNow playing: {player.now_playing}\n" \
                  f"up next: {up_next}\n" \
                  f"playing state: {vc.is_playing()}\n" \
                  "```"
        return await ctx.send(message)

    @commands.command(description="Resume playing")
    async def resume(self, ctx):
        """
        Resumes playing the paused song.

        usage:
            .resume
        """

        player = self.bot.players[ctx.guild.id]
        await player.resume()

    @commands.command(description="Search songs")
    async def search(self, ctx, *keywords):
        """
        Searches the song index for a particular song.

        usage:
            .search <keywords>
        """

        if not keywords:
            return await ctx.send("What would you like to search for?")

        results = await self.search_index(ctx, keywords)
        if results is None:
            return

        # Cut to the first 40 results due to discord character limitations
        results = results[:40]
        message = f"```css\n{ctx.author.name}, here are your song results.\n"

        counter = 1
        for i in results:
            message += f"\n{counter}: {i.name}"
            counter += 1
        message += "```"
        await ctx.send(message)

    async def search_index(self, ctx, keywords):
        """
        Searches the song index for a particular song and, if multiple are
        found, asks which one was intended.
        """

        # I think I'll bring the search class into here so it's possible to
        # search without having the bot in a voice channel.
        results = self.searcher.search(" ".join(keywords))
        if not results:
            await ctx.send("Sorry, that does not match any songs.")
            return [None, None]

        return results

    @commands.command(descrption="Stop playing")
    async def stop(self, ctx):
        """
        Stops the bot from playing it's current song and pauses the audio.

        usage:
            .stop

        This command may be removed in future updates.
        """
        player = self.bot.players[ctx.guild.id]
        await player.stop()
        await ctx.send("Stopped voice client")

    @commands.command(description="Summon bot to voice")
    async def summon(self, ctx):
        """
        Summons the bot to your voice channel

        usage:
            .summon
        """

        channel = ctx.author.voice.channel
        if not channel:
            return await ctx.send("Join a voice channel first.")

        try:
            vc = self.bot.players[ctx.guild.id].voice_client
            await vc.move_to(channel)

        except KeyError:
            return await self.initialize_voice(ctx)


async def setup(bot):
    await bot.add_cog(musicPlayer(bot))
