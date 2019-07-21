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
# import youtube_dl

from asyncio import sleep
from discord.ext import commands
from discord import client

if not discord.opus.is_loaded():
    discord.opus.load_opus("opus")


class musicPlayer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.current_vc = None
        self.player = None
        self.music_queue = []

    async def create_voice_client(self, author):
        """
        Creates a voice client for hte music player to
        use.
        """

        if not author.voice_channel:
            return await self.bot.say("Please enter a voice channel first")

        if not self.current_vc:
            return self.current_vc.move_to(author.voice_channel)

        return await self.bot.join_voice_channel(author.voice_channel)

    async def queue(self, channel, url):
        """
        Queues a song to play if a song is already playing.
        """

        self.music_queue.append(url)

        await self.bot.send_message(channel, f"```Your song is "
                                             f"{len(self.music_queue)} in the "
                                             "queue.```")

    async def play_queue(self):
        try:
            url = await self.get_url()
            self.player = await self.current_vc.create_ytdl_player(url)
            self.player.start()
            while not self.player.is_playing():
                sleep(1)

        except Exception as e:
            await self.send_error(e)

        # else:
        #     while True:
        #         if not self.player.is_playing():
        #             up_next = await self.get_url()

        #             if not up_next:
        #                 break
        #             else:
        #                 self.player = await self.current_vc.create_ytdl_player(up_next)
        #                 self.player.start()

        #                 while not self.check_playing:
        #                     sleep(1)

        #    self.player == None
            self.current_vc.disconnect()
        #    self.current_vc == None

    async def check_playing(self):
        return self.player.is_playing()

    async def get_url(self):
        if len(self.music_queue) >= 1:
            return self.music_queue.pop(0)
        else:
            return None

    async def send_error(self, error):
        await self.bot.say(f"```\nAn error has occured. Message follows....\n"
                           f"{error}\n```")

    @commands.command(pass_context=True,
                      description="Plays sound from youtube")
    async def play(self, ctx, url=None):
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

        await self.queue(ctx.message.channel, url)

        await client.Client.delete_message(self.bot, ctx.message)

        if not self.player:
            if self.player.is_playing():
                # await self.queue(channel,url)
                await self.bot.say("I'm playing currently. Queueing videos "
                                   "will be added in a future update.")

        self.current_vc = await self.create_voice_client(ctx.message.author)

        await self.play_queue()

        # else:
        #     try:
        #         self.player = await self.current_vc.create_ytdl_player(url)

        #     except Exception as e:
        #         await self.send_error(e)
        #         await self.current_vc.disconnect()

        #     self.player.start()

    @commands.command(description="Stops playing music.")
    async def stop(self):
        """
        Stops playing music.

        usage:
            .stop
        """
        self.player.stop()
        self.player = None
        await self.current_vc.disconnect()
        await self.bot.say("```\nMusic player stopped.\n```")

    @commands.command(description="Pauses music playing.")
    async def pause(self):
        """
        Pauses music.

        usage:
            .pause
        """

        self.player.pause()
        await self.bot.say("```\nMusic paused\n```")

    @commands.command(description="Resumes playing music.")
    async def resume(self):
        """
        Resumes playing paused music.

        usage:
            .resume
        """
        await self.player.start()
        await self.bot.say("```\nResuming music...\n```")

    @commands.command(description="Clears music queue.")
    async def clear(self):
        """
        Clears the music queue.

        usage:
            .clear
        """
        self.music_queue = []
        await self.bot.say("```Cleared the music queue```")

    @commands.command(pass_context=True,
                      description="Music player volume control.")
    async def set_vol(self, ctx, vol):
        """
        Attempts to set music player volume.

        The highest the player can go is to 200%.

        usage:
            set the volume to 10%
            .set_vol 10

            set the volume to 50%
            .set_vol 50
        """

        try:
            vol = int(vol)
            vol /= 100

            if vol >= 2:
                vol = 2

            self.player.volume = vol

            return await self.bot.say(f"Set player volume to {vol*100}%")

        except Exception as e:
            return await self.bot.say(f"Invalid input received, error follows:"
                                      f"\n{e}")


def setup(bot):
    bot.add_cog(musicPlayer(bot))
