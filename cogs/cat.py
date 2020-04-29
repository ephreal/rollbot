# -*- coding: utf-8 -*-

"""
Copyright (c) 2020 Ephreal under the MIT License.
To view the license and requirements when distributing this software, please
view the license at https://github.com/ephreal/catapi/LICENSE.
"""

from discord.ext import commands
from utils.message_builder import embed_catapi_image
import asyncio
import catapi


class Catapi(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api = catapi.CatApi(api_key=bot.catapi_key)

    @commands.command(description="Random cat pictures")
    async def cat(self, ctx, limit=1):
        if limit > 20:
            limit = 20

        images = await self.api.search_images(limit=limit)
        for image in images:
            reply = await embed_catapi_image(ctx, image)
            await ctx.send(embed=reply)
            await asyncio.sleep(5)


def setup(bot):
    if bot.catapi_key:
        bot.add_cog(Catapi(bot))
        print("catapi added")
    else:
        print("Cat cog not loaded: Missing bot.catapi_key")
