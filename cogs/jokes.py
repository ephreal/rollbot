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

    """
    Commands:
        .joke        - fetch a random joke
        .joke dad    - fetch a random dad joke
        .joke norris - fetch a random chuck norris joke

    Methods:
        joke(ctx: discord context object, joke_type: string):
            The main command for this module. Returns various jokes as
            determined by the joke_type parameter. Currently accepted joke
            types are chuck, norris, and dad.

        chuck_norris_joke():
            -> joke: string
            Returns a string chuck norris joke.

        dad_joke():
            -> joke: string
            Returns a string dad joke
    """

    @commands.command(description="Get a random joke")
    async def joke(self, ctx, joke_type=None):
        """
        Fetches and displays a random joke for your amusement.

        Available joke types are
            dad
            chuck
            norris

        Get a random joke:
            .joke

        Get a dad joke:
            .joke dad

        Get a chuck norris joke:
            .joke chuck
        """

        if joke_type == "dad":
            return await ctx.send(await self.dad_joke())
        elif joke_type == "chuck" or joke_type == "norris":
            return await ctx.send(await self.chuck_norris_joke())

        return await ctx.send(await self.dad_joke())

    async def chuck_norris_joke(self):
        """
        Gets and returns a chuck norris joke.

            -> joke: string
        """

        url = "https://api.icndb.com/jokes/random"

        norris_joke = await network.fetch_page(url)
        norris_joke = json.loads(norris_joke)
        return norris_joke["value"]["joke"]

    async def dad_joke(self):
        """
        Gets and returns a dad joke from https://icanhazdadjoke.com

            -> joke: String
        """

        headers = {"Accept": "application/json"}
        url = "https://icanhazdadjoke.com"
        dad_joke = await network.fetch_page(url, headers)
        dad_joke = json.loads(dad_joke)
        return dad_joke["joke"]


def setup(bot):
    bot.add_cog(Joke(bot))
