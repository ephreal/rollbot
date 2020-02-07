# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""


import discord
import os
# Note: The import here is going to be relative to the main.py file, not this
#       one. Therefore, look in a utils folder near main.py. I really wish I
#       knew a better way to do this.
from utils.structures import Queue


class MusicPlayer():
    """
    A music player object to make management of music from the bot easier.
    This will be wrapping a lot of discord.VoiceClient commands to make my
    life dealing with it a lot easier. Mainly because I don't know what I'm
    doing with the voice client quite yet.
    """
    def __init__(self, audio_path="audio", voice_client=None):
        # Note: Audio path will be relative to main.py
        self.audio_path = audio_path
        self.voice_client = voice_client
        self.currently_playing = None
        self.music_queue = Queue(10)

    async def available_songs(self, subdir=""):
        """
        Gets a list of available songs in audio_path.
        Future plans are for this to be indexed for easy access and not needing
        to search subdirectories manually.

        subdir: string

            -> list[string]
        """

        subdir = subdir.replace("..", "")
        path = f"{self.audio_path}/{subdir}"

        return os.listdir(path)

    async def clear(self):
        """
        Clears the music queue
        """

        await self.music_queue.clear()

    async def enqueue(self, song):
        """
        Adds a song to the music queue.
        """

        song = song.replace("..", "")
        song = f"{self.audio_path}/{song}"
        if not await self.music_queue.add(song):
            return None

        if not self.voice_client.is_playing():
            await self.play()

        return True

    async def next(self):
        """
        Advance the music player to the next song. If there is no song up next,
        the music player will stop playing.
        """

        if not await self.music_queue.peek():
            return None
        await self.voice_client.stop()
        await self.play()

    async def pause(self):
        """
        Pauses the currently playing song. Little more than a wrapper for
        voice_client.pause

            -> None
        """

        self.voice_client.pause()

    async def play(self):
        """
        Plays the song up next on the queue.
        """

        song = await self.music_queue.remove()
        # Can only play local files for now.
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(song))
        self.voice_client.play(source)

    async def stop(self):
        """
        Stops any currently playing music. Does not re-add that song to the
        music queue.
        """

        self.voice_client.stop()

    async def up_next(self):
        """
        Gets the song that is up next. Returns None if no song is up next.

            -> String or None
        """

        return await self.music_queue.peek()