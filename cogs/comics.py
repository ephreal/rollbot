# -*- coding: utf-8 -*-

"""
Copyright 2018-2019 Ephreal

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

import json
import random

from discord.ext import commands
from utils import network


class Comics(commands.Cog):
    def __init__(self, bot=None):
        self.bot = bot

    @commands.command(description="Fetches webcomics")
    async def comic(self, ctx, comic=None, comic_num=None):
        """
        Fetches a webcomic and places a link to the comic picture in
        the chat. If no comic is provided, this will fetch a random xkcd comic.

        currently supported comics are

        sromg
        xkcd

        examples:
            Get xkcd comic 101
            .comic xkcd 101
        """

        if comic is None:
            comic = "sromg"

        if comic == "sromg":
            url = await self.fetch_sromg(comic_num)

        elif comic == "xkcd":
            url = await self.fetch_xkcd(comic_num)

        await ctx.send(url)

    async def fetch_sromg(self, comic_num=None):
        """
        Fetches an sromg comic if comic_num is not None.
        Fetches a random comic if comic_num is None.

        comic_num: int
            -> comic_url: String
        """

        comic_url = "https://mezzacotta.net/garfield/"
        if not comic_num:
            # This is very brittle and will break if the website ever changes.
            # They don't seem to have an API though... so.... oh well?
            # Also, something is breaking aiohttp with this site... wierd
            latest = await network.non_aiohttp_fetch(comic_url)
            latest = latest.decode()
            comic_index = latest.index("<h2>No. ") + 8
            latest = latest[comic_index:comic_index + 4]

            comic_num = str(random.randint(1, int(latest)))

        return f"{comic_url}comics/{comic_num.zfill(4)}.png"

    async def fetch_xkcd(self, comic_num):
        """
        Fetches an sromg comic if comic_num is not None.
        Fetches a random comic if comic_num is None.

        comic_num: int
            -> comic_url: String
        """

        latest = await network.fetch_page("https://xkcd.com/info.0.json")
        latest = json.loads(latest)

        if comic_num:
            try:
                xkcd_num = int(comic_num)
                if xkcd_num > latest["num"]:
                    xkcd_num = latest["num"]
                elif xkcd_num < 1:
                    xkcd_num = 1
            except ValueError:
                xkcd_num = random.randint(1, latest["num"])
        else:
            xkcd_num = random.randint(1, latest["num"])

        return f"https://xkcd.com/{xkcd_num}"

    @commands.command(description="SROMG comic")
    async def sromg(self, ctx, comic_num=None):
        """
        Gets and SROMG comic. By default, this grabs a random comic.

        Examples:
            Get a random comic
            .sromg

            get comic number 404
            .sromg 404
        """
        comic_url = await self.fetch_sromg(comic_num)
        await ctx.send(comic_url)

    @commands.command(description="gets an XKCD webcomic")
    async def xkcd(self, ctx, comic_num=None):
        """
        Gets an XKCD comic. By default, will grab a random comic.

        Examples:
            Get a random webcomic
            .xckd

            Get comic number 404
            .xkcd 404
        """

        comic_url = await self.fetch_xkcd(comic_num)
        await ctx.send(comic_url)


def setup(bot):
    bot.add_cog(Comics(bot))
