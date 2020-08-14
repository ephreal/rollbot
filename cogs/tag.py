# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

from discord.ext import commands
from utils.checks import check_author
from utils import message_builder


class Tag(commands.Cog):
    """Provides an interface to allow users to tag custom content."""

    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db_handler.tags

    @commands.command(description="Tag content")
    async def tag(self, ctx, *tag):
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

        if tag[0] == "delete":
            tag = " ".join(list(tag)[1:])
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
            tag = " ".join(tag)
            message = await self.db.fetch_tag(ctx.author.id, tag)
            if not message:
                message = await self.create_tag(ctx, tag)

        if message:
            return await ctx.send(message)

    @commands.command(description="Tag content")
    async def gtag(self, ctx, *tag):
        """Tag content for later use

        Tagging content allows you to save some data in an easy to remember tag
        and call it back at a later time whenever you'd like.

        Unlike the tag command, gtag is available to everyone in the guild to
        use. This means that other users have the capability to modify or
        delete any tags you use here at any time. If you wish to keep your
        tags safe(er), use the tag command.

        Examples
        --------

        Create a tag called greeting:
            .gtag greeting

        Have the bot print out the contents of greeting
            .gtag greeting

        Delete the tag greeting
            .gtag delete greeting
        """

        if tag[0] == "delete":
            tag = " ".join(list(tag)[1:])
            await self.db.delete_guild_tag(ctx.guild.id, tag)
            return await ctx.send(f"{tag} has been deleted")

        if not tag:
            author = ctx.message.author
            await ctx.send("What would you like your tag to be?")
            tag = await self.bot.wait_for('message', timeout=60,
                                          check=check_author(author))
            tag = tag.content
            message = await self.create_guild_tag(ctx, tag)

        else:
            tag = " ".join(tag)
            message = await self.db.fetch_guild_tag(ctx.guild.id, tag)
            if not message:
                message = await self.create_guild_tag(ctx, tag)

        if message:
            return await ctx.send(message)

    @commands.command()
    async def tags(self, ctx, page=1):
        """
        Gets 25 of your tags that you have defined. To see additional tags,
        pass in the page number to the command.

        Example
        -------

        Get your first 25 tags
            .tags

        get tag numbers 50-75
            .tags 2
        """

        try:
            page = int(page)
        except ValueError:
            page = 1
        except TypeError:
            page = 1

        page -= 1

        message = ["```\nYour tags are:\n"]

        tags = await self.db.fetch_all_tags(ctx.author.id, page)
        if not tags:
            message.append("You have no tags")
        else:
            message.append("\n".join(tags))

        message.append("```")
        message = "\n".join(message)
        message = await message_builder.embed_reply(ctx.author, message)
        message.set_footer(text="run 'tags <pagenumber> to view more results'")
        await ctx.send(embed=message)

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

    @commands.command()
    async def gtags(self, ctx, page=1):
        """
        Gets 25 guild tags that are currently defined

        Example
        -------

        Get the first 25 guild tags
            .gtags

        get tags number 50-75
            .gtags 2
        """

        try:
            page = int(page)
        except ValueError:
            page = 1
        except TypeError:
            page = 1

        page -= 1

        message = ["```\nGuild Tags\n==========\n"]
        tags = await self.db.fetch_all_guild_tags(ctx.guild.id, page)
        if not tags:
            message.append("Your guild has no tags")
        else:
            message.append("\n".join(tags))
        message.append("```")
        message = "\n".join(message)
        message = await message_builder.embed_reply(ctx.author, message)
        await ctx.send(embed=message)

    async def create_guild_tag(self, ctx, tag):
        author = ctx.message.author

        await ctx.send(f"What would you like '{tag}' to contain?\n"
                       "Reply 'cancel' to cancel")

        msg = await self.bot.wait_for('message', timeout=600,
                                      check=check_author(author))
        if msg.content == "cancel":
            await ctx.send("Cancelling")
            return ""

        msg = msg.content
        await self.db.create_guild_tag(ctx.guild.id, tag, msg)
        return f"{tag} has been created"


def setup(bot):
    bot.add_cog(Tag(bot))
