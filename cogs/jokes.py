# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""


from discord.ext import commands
from classes.utils import network

import json


class Joke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Get a random joke")
    async def joke(self, ctx):
        """
        Fetches and displays a random joke for your amusement.
        """

        await ctx.send(await self.chuck_norris_joke(), tts=True)

    async def chuck_norris_joke(self):
        """
        Gets and returns a chuck norris joke.
        """

        url = "https://api.icndb.com/jokes/random"

        norris_joke = await network.fetch_page(url)
        norris_joke = json.loads(norris_joke)
        return norris_joke["value"]["joke"]

def setup(bot):
    bot.add_cog(Joke(bot))
