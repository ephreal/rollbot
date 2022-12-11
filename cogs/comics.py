# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

import json
import random

from discord.ext import commands
from utils import network


class Comics(commands.Cog):
    """
    Commands provided by this module

    .sromg
    .xkcd
    """
    def __init__(self, bot=None):
        self.bot = bot

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
        Fetches an xkcd comic if comic_num is not None.
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


async def setup(bot):
    await bot.add_cog(Comics(bot))
