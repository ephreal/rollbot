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

import random
from asyncio import sleep
from discord import client
from discord.ext import commands


class admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True,
                      description="Deletes messages")
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx, limit: int, flags=""):
        """
        Purges a channel of a specified amount of messages. Currently no limit
        is set, but the discord library may have an upper limit.
        Requires administrator permissions to run

        Examples:
            purge 10 messages
            .purge 10

            purge 10 messages including all attachments
            .purge 10 all
        """

        await ctx.message.delete()
        if "all" in flags:
            await ctx.message.channel.purge(limit=limit)
        else:
            await ctx.message.channel.purge(limit=limit,
                                            check=lambda msg: not msg.pinned
                                            and not msg.attachments)

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You must be an administrator to use this command.")
        else:
            await ctx.send("Something is wrong with your command.\n"
                           f"Error message: {error}")

    @commands.command(hidden=True,
                      description="Shuts down the bot")
    @commands.has_permissions(administrator=True)
    async def halt(self, ctx):
        """
        Shuts the bot down.
        Requires administrator permissions to run.

        usage: .halt
        """

        shutdown_message = "The bot is currently shutting down. Good bye"
        shutdown_message = shutdown_message[0:random.randint(0,
                                            len(shutdown_message)-1)]

        await ctx.send(f"{shutdown_message}"+shutdown_message[-1]*4+"....")
        await client.Client.logout(self.bot)

    @halt.error
    async def halt_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You must be an administrator to use this command.")
        else:
            await ctx.send("Something is wrong with your command.\n"
                           f"Error message: {error}")

    @commands.command(hidden=True,
                      description="Channel message spammer")
    @commands.has_permissions(administrator=True)
    async def spam(self, ctx):
        """
        Spams messges to a channel.

        Sometimes you need to test things on a large amount of
        messages. For those times, the spam command will be
        your friend. Instead of having to individually create
        hundreds of messages, why not have a bot do it for you?

        The maximum amount of messages allowed is 1000.

        Requires administrator permissions to run.

        usage:
            send 10 messages to a channel
                .spam or .spam 10

            send 200 messages to a channel
                .spam 200
        """

        command = ctx.message.content.split()
        command = command[1:]

        try:
            if len(command) == 0:
                amount = 10
            else:
                amount = int(command[0])

            if amount > 1000:
                return await ctx.send("I can't spam more than 1000 messages "
                                      "at a time. Please try again.")

            for i in range(0, amount):
                await ctx.send(f"Message {i}.")
                await sleep(1)

        except Exception as e:
            await ctx.send("Invalid input received.")
            await ctx.send(f"Error follows:\n{e}")

    @spam.error
    async def spam_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You must be an administrator to use this command.")
        else:
            await ctx.send("Something is wrong with your command.\n"
                           f"Error message: {error}")


def setup(bot):
    bot.add_cog(admin(bot))
