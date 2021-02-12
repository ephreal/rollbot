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
        self.sessions = []

    @commands.command()
    async def connect(self, ctx):
        if await self.check_dupes(ctx):
            return
        message, embed = await self.initialize(ctx)
        await self.get_welcome_message(embed)
        await message.edit(embed=embed)
        name = await self.get_bbs_username(ctx, message, embed)
        if name is None:
            await self.cleanup(ctx)
            return
        await self.mainloop(ctx)
        await self.cleanup(ctx)

    async def mainloop(self, ctx):
        await ctx.send("This is not yet functional")

    async def cleanup(self, ctx):
        self.sessions.remove(ctx.author.id)

    async def check_dupes(self, ctx):
        if ctx.author.id in self.sessions:
            message = "Error, duplicate session detected."
            embed = await message_builder.embed_reply(ctx.author, message)
            await ctx.send(embed=embed)
            return True
        else:
            self.sessions.append(ctx.author.id)

    async def initialize(self, ctx):
        connect_time = 0.25
        initialization = self.shadowland_strings['connection']
        message = initialization[0]
        embed = message_builder.embed_reply_no_author(message)
        initialization = initialization[1:]
        sent_message = await ctx.channel.send(embed=embed)

        for part in initialization:
            await asyncio.sleep(connect_time)
            message += part
            embed = message_builder.embed_reply_no_author(message)
            await sent_message.edit(embed=embed)

        return sent_message, embed

    async def get_welcome_message(self, embed):

        message = f"\n{self.shadowland_strings['welcome_message']}: "
        tag = random.choice(self.shadowland_strings['welcome_tags'])
        message = f"{message}: {tag}"
        embed.description = f"{embed.description}{message}"

    async def get_bbs_username(self, ctx, message, embed):
        name = await self.db.get_bbs_username(ctx.guild.id, ctx.author.id)
        if not name:
            name = await self.add_user(ctx, message, embed)
            if name is None:
                return
        return name[0][0]

    async def add_user(self, ctx, message, embed):
        notification = "Unknown connection. Please input a username"
        embed.description = f"{embed.description}\n{notification}"
        await message.edit(embed=embed)
        try:
            name = await self.get_response(ctx)
            name = name.content
        except asyncio.TimeoutError:
            fail = "No input detected for 60 seconds. User either dead or " \
                   "bored. Closing connection......"
            embed.description = f"{embed.description}\n{fail}"
            await message.edit(embed=embed)
            return

        await self.db.add_user(ctx.guild.id, ctx.author.id, name)

        notification = f"\nUser: {name}\nConnection..... Stable."
        embed.description = f"{embed.description}{notification}"
        await message.edit(embed=embed)

        return name

    async def get_response(self, ctx):
        def check(m):
            return (m.author == ctx.message.author and
                    m.channel == ctx.message.channel)

        return await self.bot.wait_for('message', check=check, timeout=60)


def setup(bot):
    bot.add_cog(shadowland(bot))
