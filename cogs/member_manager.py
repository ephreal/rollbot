# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

from discord.ext import commands
from discord import Embed
from discord import Colour


class MemberManager(commands.Cog):
    """
    Commands provided by this cog

    .ban
    .kick
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="ban a user")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, banee, *reason):
        """
        Bans a user from the guild.

        A message will be sent to both the person being banned to let them know
        they are now banned, and a message will be sent to the person doing the
        banning upon completion.

        A reason for banning a member is required and must be provided.

            Examples:
                Ban Joe because he keeps asking for picture of trains
                    .ban joe You keep asking for train pictures. Why??

                Ban Joe by user id
                    .ban joe#0000 Seriously, how did you get back in?
        """

        member = ctx.guild.get_member_named(banee)

        if not ctx.guild.me.guild_permissions.ban_members:
            await ctx.send("This bot requires the ban members permission "
                           "in order to do that. Please assign it the correct "
                           "permissions and try again.")

        if not member:
            return await ctx.send("That user cannot be found, did you "
                                  "capitalize properly?")

        elif not reason:
            return await ctx.send("A reson for kicking must be provided")

        message = Embed()
        message.title = f"You've been banned from {ctx.guild.name}"
        message.description = f"You were banned because:\n{' '.join(reason)}"
        message.colour = Colour.from_rgb(255, 0, 0)
        await ctx.send(embed=message)

        await ctx.guild.ban(member)
        await ctx.author.send(f"{member} has been banned from the guild.")

    @commands.command(description="kick a user")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, kickee, *reason):
        """
        Kicks a user from the guild.

        A message will be sent to both the person being kicked and the person
        doing the kicking.

        A reason for kicking a user is required and must be provided.

        Examples:
            Kick Joe from the guild because he's loud
            .kick joe You are too loud.

            Kick joe with his userid
            .kick joe#0000 Please stop joining this guild.
        """

        member = ctx.guild.get_member_named(kickee)

        if not ctx.guild.me.guild_permissions.kick_members:
            await ctx.send("This bot requires the kick members permission "
                           "in order to do that. Please assign it the correct "
                           "permissions and try again.")

        if not member:
            return await ctx.send("That user cannot be found, did you "
                                  "capitalize properly?")
        elif not reason:
            return await ctx.send("A reson for kicking must be provided")

        message = Embed()
        message.title = f"You've been kicked from {ctx.guild.name}"
        message.description = f"You were kicked because:\n{' '.join(reason)}"
        message.colour = Colour.from_rgb(255, 255, 0)
        await member.send(embed=message)

        await ctx.guild.kick(member)
        await ctx.author.send(f"{member} has been kicked from the guild.")


async def setup(bot):
    await bot.add_cog(MemberManager(bot))
