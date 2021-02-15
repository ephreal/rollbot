# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

from discord import Embed, TextChannel
from discord.ext import commands


class MessageManager(commands.Cog):
    """
    commands:
        move(limit, text_channel):
            moves limit amount of messages from one text channel to another
        purge(limit):
            purges limit amount of messages from a channel
    """
    def __init__(self, bot):
        self.bot = bot
        self.prefix = self.bot.command_prefix

    @commands.command(description="Move a specified amount of messages")
    @commands.has_permissions(manage_messages=True)
    async def move(self, ctx, limit: int, channel: TextChannel):
        """
        Moves a specified amount of messages to the specified channel.

        usage:
            .move <amount> #channel-name

        examples:
            move 10 messages to the questions-chat-1 channel
            .move 10 #questions-chat-1
        """

        # Clear the bot command message
        await ctx.message.delete()

        messages = []
        async for message in ctx.message.channel.history(limit=limit):
            embed = Embed(description=message.content)

            embed.set_author(name=message.author.name,
                             icon_url=message.author.avatar_url)

            embed.timestamp = message.created_at
            messages.append(embed)
            await message.delete()

        for i in messages[::-1]:
            await channel.send(embed=i)

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

        with ctx.typing():
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
