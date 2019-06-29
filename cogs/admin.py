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
import json
import random
from asyncio import sleep
from discord import client
from discord.ext import commands


class admin:
    def __init__(self, bot):
        self.bot = bot
        self.admins = []
        with open("config/config.json", 'r') as f:
            self.admin_group = json.load(f)["admin_group"]
        # self.admin_group = "Admins"
        # self.admin_group = self.get_admins(ctx)

    @commands.command(pass_context=True, hidden=True)
    async def purge(self, ctx):
        """
        Removes X amount of messages from the channel the command is
        ran in. Currently limited to 100 messages at a time. This
        will default to removing 10 messages at a time.

        Message purging ignores any pinned messages or messages with
        attachments by default. To purge everything, include "all"
        after in your purge command.

        usage examples:

            purge 10 messages:  .purge  OR  .purge 10
            purge 100 messages: .purge 100

            purge 100 messages (including messages with attachments/pins)
                .purge 100 all

            purge 1000 messages (including messsges with attachments/pins)
                .purge all  or  .purge 1000 all
        """

        author_id = ctx.message.author.id

        # Get admins
        await self.get_admins(ctx)

        # Only allow admins to run admin commands
        if author_id not in self.admins:
            return await self.bot.say("That command is restricted to admins.")

        channel = ctx.message.channel
        msgs = []
        limit = ctx.message.content.split()

        if len(limit) == 1:
            limit = 10
        elif limit[1] == "all":
            limit = 1000
        elif len(limit) >= 2:
            limit = int(limit[1])

        async for x in client.Client.logs_from(self.bot, channel, limit=limit):
            msgs.append(x)

        if not "all" in ctx.message.content:

            # check for pinned messages
            to_keep = await client.Client.pins_from(self.bot, channel)
            to_keep = [x.id for x in to_keep]

            # Check msgs for any to_keep messages or messages
            # with attachments and do not delete them.

            for x in msgs:
                if x.id in to_keep:
                    msgs.remove(x)

                elif x.attachments:
                    msgs.remove(x)

        # delete messages in groups of 100 at a time
        while msgs:
            await client.Client.delete_messages(self.bot, msgs[0:100])
            msgs = msgs[100:]

    @commands.command(hidden=True, pass_context=True)
    async def halt(self, ctx):
        """
        halts the bot

        usage: .halt
        """

        shutdown_message = "The bot is currently shutting down. Good bye"
        shutdown_message = shutdown_message[0:random.randint(0,
                                            len(shutdown_message)-1)]

        author_id = ctx.message.author.id

        if not self.admins:
            await self.get_admins(ctx)

        if author_id not in self.admins:
            return await self.bot.say("Only admins may halt me.")

        await self.bot.say(f"{shutdown_message}"+shutdown_message[-1]*4+"....")
        await client.Client.logout(self.bot)

    @commands.command(pass_context=True)
    async def refresh_admins(self, ctx):
        """
        Reloads admin group membership

        usage: .refresh_admins
        """
        await self.get_admins(ctx)
        await self.bot.send_message(ctx.message.author, "Admin list refreshed")

    @commands.command(pass_context=True,
                      hidden=True,
                      description="Channel message spammer")
    async def spam(self, ctx):
        """
        Spams messges to a channel.

        Sometimes you need to test things on a large amount of
        messages. For those times, the spam command will be
        your friend. Instead of having to individually create
        hundreds of messages, why not have a bot do it for you?

        The maximum amount of messages allowed is 1000.

        usage:
            send 100 messages to a channel
                .spam or .spam 100

            send 200 messages to a channel
                .spam 200
        """

        author_id = ctx.message.author.id

        if not self.admins:
            await self.get_admins(ctx)

        if not author_id in self.admins:
            return await self.bot.say("This command is for admins only.")

        command = ctx.message.content.split()
        command = command[1:]

        try:
            if len(command) == 0:
                amount = 100
            else:
                amount = int(command[0])

            if amount > 1000:
                return await self.bot.say("Messages to spam is over 1000")

            for i in range(0, amount):
                await self.bot.say(f"Message {i}.")
                await sleep(1)

        except Exception as e:
            await self.bot.say("Invalid input received.")
            await self.bot.say(f"Error follows:\n{e}")

    async def get_admins(self, ctx):
        """
        Gets a list of admins from the server and places them in
        self.admins. If no admins are found, it sends a message
        to the channel warning the user that the admin group has
        no users.

        If no admins are found, it's also possible the the admin
        group does not exist and must be created.

        To change the admin group, modify the self.admins in the
        class definition.

        Default admin group: Admins
        """
        role = discord.utils.get(ctx.message.server.roles,
                                 name=self.admin_group)
        for member in ctx.message.server.members:
            if role in member.roles:
                self.admins.append(member.id)

        if len(self.admins) == 0:
            message = f"No admins found. Is there a \"{self.admin_group}\""\
                      "group with users?\n(Note: Group name is case sensitive)"

            await self.bot.send_message(ctx.message.channel, message)


def setup(bot):
    bot.add_cog(admin(bot))
