# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

from discord.ext import commands
from utils.checks import check_author


class Tag(commands.Cog):
    """Provides an interface to allow users to tag custom content."""

    def __init__(self, bot):
        self.bot = bot
        self.db = bot.tag_db

    @commands.command(description="Tag content")
    async def tag(self, ctx, tag=None, delete_tag=None):
        """Tag content for later use

        Tagging content allows you to save some data in an easy to remember tag
        and call it back at a later time whenever you'd like.

        Examples
        --------

        Create a tag called greeting:
            .tag greeting

        Have the bot print out the contents of greeting
            .tag greeting

        Delete the tag greeting
            .tag delete greeting
        """

        if tag == "delete":
            tag = delete_tag
            await self.db.delete_tag(ctx.author.id, tag)
            return await ctx.send(f"{tag} has been deleted")

        if not tag:
            author = ctx.message.author
            await ctx.send("What would you like your tag to be?")
            tag = await self.bot.wait_for('message', timeout=60,
                                          check=check_author(author))
            tag = tag.content
            message = await self.create_tag(ctx, tag)

        else:
            message = await self.db.fetch_tag(ctx.author.id, tag)
            if not message:
                message = await self.create_tag(ctx, tag)

        if message:
            return await ctx.send(message)

    @commands.command()
    async def tags(self, ctx):
        """
        Gets all tags you currently have defined.

        Example
        -------

        Get all your tags
            .tags
        """

        tags = await self.db.fetch_all_tags(ctx.author.id)
        if not tags:
            await ctx.send("You have no tags")
        else:
            tags = "\n".join(tags)
            await ctx.send(f'Your tags are: \n{tags}')

    async def create_tag(self, ctx, tag):
        author = ctx.message.author

        await ctx.send(f"What would you like '{tag}' to contain?\n"
                       "Reply 'cancel' to cancel")

        msg = await self.bot.wait_for('message', timeout=600,
                                      check=check_author(author))
        if msg.content == "cancel":
            await ctx.send("Cancelling")
            return ""

        msg = msg.content
        await self.db.create_tag(ctx.author.id, tag, msg)
        return f"{tag} has been created"


def setup(bot):
    bot.add_cog(Tag(bot))
