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

from discord.ext import commands
from discord import Embed


class MemberManager(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="kick a user")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, kickee, *reason):
        """
        Kicks a user from the guild. A message will be sent to both the
        person being kicked and the person doing the kicking.

        Examples:
            Kick Joe from the guild
            .kick joe

            Kick joe with his userid
            .kick joe#0000
        """

        member = ctx.guild.get_member_named(kickee)

        if not ctx.guild.me.guild_permissions.kick_members:
            await ctx.send("This bot requires the kick members permission "
                           "in order to do that. Pleas assign it the correct "
                           "permissions and try again.")

        if not member:
            return await ctx.send("That user cannot be found, did you "
                                  "capitalize properly?")
        elif not reason:
            return await ctx.send("A reson for kicking must be provided")

        message = Embed()
        message.title = f"You've been kicked from {ctx.guild.name}"
        message.description = f"You were kicked because:\n{' '.join(reason)}"
        await member.send(embed=message)

        await ctx.guild.kick(member)
        await ctx.author.send(f"{member} has been kicked from the guild.")


def setup(bot):
    bot.add_cog(MemberManager(bot))
