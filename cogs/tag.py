# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

from discord.ext import commands


class Tag(commands.Cog):
    """Provides an interface to allow users to tag custom content."""

    def __init__(self, bot):
        self.bot = bot
        self.db = bot.tag_db
        self.db.init_tables()

    @commands.command(description="Tag content")
    async def tag(self, ctx, tag, *content):
        """Tag content for later use

        Tagging content allows you to save some data in an easy to remember tag
        and call it back at a later time whenever you'd like.

        Examples
        --------

        Create a tag called greeting with the contents "Hello there!":
            .tag greeting Hello there!

        Have the bot print out the greeting
            .tag greeting

        Delete the tag greeting
            .tag delete greeting
        """

        if tag == "delete":
            tag = content[0]
            await self.db.delete_tag(ctx.author.id, tag)
            return await ctx.send(f"{tag} has been deleted")

        if content:
            content = " ".join(content)
            await self.db.create_tag(ctx.author.id, tag, content)
            await ctx.send(f"{tag} has been updated")

        else:
            message = await self.db.fetch_tag(ctx.author.id, tag)
            if not message:
                return await ctx.send(f"You have no tag: {tag}")
            return await ctx.send(message)


def setup(bot):
    bot.add_cog(Tag(bot))
