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

from asyncio import sleep
from discord.ext import commands


class tests(commands.Cog):
    """
    Commands

    .all_info
    .get_guilds
    .get_roles
    .info
    .ping
    .users
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def all_info(self, ctx):
        """
        Gets server information

        Shows you what channels are currently on the server
        and who your server's members are.

        Note: This command has a built in slowdown in
        returning the user data. This is because there can
        be a lot of information, and the bot WILL be rate
        limited if the slowdown is not enforced.

        usage: .all_info
        """

        channels = ctx.message.guild.channels
        channels = [{channel.name: channel.id} for channel in channels]

        await ctx.send("Channels:")

        for channel in channels:
            message = await self.format_channel(channel)
            await ctx.send(message)
            await sleep(1)

        users = ctx.message.guild.members
        users = [{member.name: [member.id, member.roles]} for member in users]

        await ctx.send("Users:\n")

        for user in users:
            message = await self.format_user(user)
            await ctx.send(message)
            await sleep(1)
        await ctx.send("All info complete.")

    @commands.command(hidden=True)
    async def get_guilds(self, ctx):
        guilds = [guild.name for guild in self.bot.guilds]
        guilds = "\n".join(guilds)
        await ctx.send(f"I am currently in {len(self.bot.guilds)} guilds.\n"
                       f"The guilds are {guilds}\n")

    @commands.command(hidden=True)
    async def get_roles(self, ctx):
        await ctx.send(ctx.guild.roles)

    async def format_channel(self, channel):
        """
        Takes a dictionary of {"channel name" : "channel id"}.
        Returns a formatted message to send back.
        """
        name = list(channel.keys())[0]
        channel_message = "```CSS\n"
        channel_message += f"\tName : {name}\n"
        channel_message += f"\tID   : {channel[name]}\n```"
        return channel_message

    async def format_user(self, user):
        """
        Takes a dictionary of {member name : member info} where
        member info is a list. Member info contains
        [member id, member roles].

        Returns a formatted message to send.
        """

        username = list(user.keys())[0]
        user_id = user[username][0]
        roles = [role.name for role in user[username][1]]
        roles.remove("@everyone")

        user_message = f"```CSS\nName: {username}\n"
        user_message += f"\tID:    {user_id}\n"
        user_message += f"\tRoles: {roles}\n```"
        return user_message

    @commands.command(hidden=True)
    async def info(self, ctx):
        """
        Basic server, channel, and user info

        This is the shortened version of the .all_info command.

        It does not return as much information as .all_info, but
        it dows give you a quick and dirty rundown of server
        info, current channel info, and your user info.

        usage: .info
        """
        info = {
                "server":      ctx.message.guild,
                "server_id":   ctx.message.guild.id,
                "channel":     ctx.message.channel,
                "channel_id":  ctx.message.channel.id,
                "author":      ctx.message.author,
                "author_id":   ctx.message.author.id
               }

        message = f"""```CSS
server:     {info['server']}
server id:  {info['server_id']}
channel:    {info['channel']}
channel id: {info['channel_id']}
author:     {info['author']}
author id:  {info['author_id']}
```
"""
        await ctx.send(message)

    @commands.command(description="Bot connectivity test")
    async def ping(self, ctx):
        """
        Checks bot availability

        Ping lets you know if the bot can hear and respond
        to you. In usual network fashion, a ping receives
        a pong packet in response.

        usage: .ping
        """
        await ctx.send("pong!")

    @commands.command(description="Gives a usercount")
    async def users(self, ctx):
        users = ctx.message.guild.members

        await ctx.send(f"There are {len(users)} members in this guild.")


async def setup(bot):
    await bot.add_cog(tests(bot))
