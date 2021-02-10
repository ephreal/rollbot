# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""


import asyncio
import random
from discord.ext import commands
from utils import message_builder


# I HATE the idea of having code that I can't really test... but this
# bbs board is probably going to be one that I can't. I don't even know where
# to begin with getting things to work the way I'd like.
class shadowland(commands.Cog):
    """
    Commands provided by shadowland:
        connect:
            connects the user to the shadowland bbs.
    """
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db_handler.shadowland
        self.shadowland_strings = bot.shadowland_strings

    @commands.command()
    async def connect(self, ctx):
        await self.greet(ctx)

    async def greet(self, ctx):
        connect_time = 0.25
        greeting = self.shadowland_strings['connection']
        message = greeting[0]
        embed = message_builder.embed_reply_no_author(message)
        greeting = greeting[1:]
        sent_message = await ctx.channel.send(embed=embed)

        for part in greeting:
            await asyncio.sleep(connect_time)
            message += part
            embed = message_builder.embed_reply_no_author(message)
            await sent_message.edit(embed=embed)

        message += f"\n{self.shadowland_strings['welcome_message']}: "
        tag = random.choice(self.shadowland_strings['welcome_tags'])
        message += tag
        embed = message_builder.embed_reply_no_author(message)
        await asyncio.sleep(connect_time)
        await sent_message.edit(embed=embed)


def setup(bot):
    bot.add_cog(shadowland(bot))
