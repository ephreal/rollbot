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


Commands provided by this cog
    purge : remove messages from a channel.
"""

from discord.ext import commands


class MessageManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefix = self.bot.command_prefix

    @commands.command(description="Deletes messages")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, limit: int, flags=""):
        f"""
        Purges a channel of a specified amount of messages. Currently no limit
        is set, but the discord library may have an upper limit.
        Requires manage_messages permissions to run

        Examples:
            purge 10 messages
            {self.prefix}purge 10

            purge 10 messages including all attachments
            {self.prefix}purge 10 all
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


def setup(bot):
    bot.add_cog(MessageManager(bot))
