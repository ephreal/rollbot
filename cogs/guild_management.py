# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""


from discord import Colour
from discord import Permissions
from discord.ext import commands


class GuildManager(commands.Cog):
    """
    Commands
    .bottester
        Adds the bottester role to the user
    create_channels
        Creates all text channels needed for full use of this bot
    create_roles
        Creates all roles needed for full use of this bot
    nsfw
        Adds the nsfw role to a user so they can access the nsfw channel
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bottester(self, ctx):
        """
        Adds the bottester role to the user
        """

        bottester = ctx.guild.roles
        bottester = [role for role in bottester if role.name == "bottester"]
        bottester = bottester[0]
        await ctx.author.add_roles(bottester)

    @commands.has_permissions(manage_guild=True)
    @commands.command()
    async def create_channels(self, ctx):
        """
        Creates all the text channels that the server should have by default
        for this bot to fully function.
        """
        channels = ["bottesting", "nsfw", "rolling", "tabletop"]
        category = ctx.guild.categories
        category = [i for i in category if i.name == "Text Channels"]
        category = category[0]

        guild_channels = ctx.guild.text_channels
        guild_channels = [channel.name for channel in guild_channels]

        for channel in channels:
            if channel not in guild_channels:
                if channel == 'nsfw':
                    await ctx.guild.create_text_channel(channel,
                                                        category=category,
                                                        nsfw=True)
                else:
                    await ctx.guild.create_text_channel(channel,
                                                        category=category)
        await ctx.send("Created text channels!")

    @commands.command(description="Setup roles for bot")
    @commands.has_permissions(manage_guild=True)
    async def create_roles(self, ctx):
        if not ctx.guild.me.guild_permissions.manage_roles:
            return await ctx.send("I need the manage roles permission.")

        role_reason = "This role was auto-created by a bot because the role "\
                      "was missing from the guild."

        admin_colour = Colour.from_rgb(218, 245, 66)
        mod_colour = Colour.from_rgb(214, 77, 13)
        guildmate_colour = Colour.from_rgb(98, 227, 43)
        lurker_colour = Colour.from_rgb(43, 227, 215)
        unverified_colour = Colour.from_rgb(215, 45, 227)

        admin_permissions = Permissions(2146958583)
        mod_permissions = Permissions(1341652163)
        guildmate_permissions = Permissions(133684289)
        lurker_permissions = Permissions(36822081)
        unverified_permissions = Permissions(84992)

        current_roles = ctx.guild.roles
        current_roles = [role.name for role in current_roles]

        if "admins" not in current_roles:
            await ctx.guild.create_role(name="admins",
                                        permissions=admin_permissions,
                                        colour=admin_colour,
                                        mentionable=True,
                                        hoist=True,
                                        reason=role_reason)
        if "bottester" not in current_roles:
            await ctx.guild.create_role(name="bottester",
                                        permissions=unverified_permissions,
                                        color=unverified_colour,
                                        mentionable=False,
                                        hoist=False,
                                        reason=role_reason)
        if "mods" not in current_roles:
            await ctx.guild.create_role(name="mods",
                                        permissions=mod_permissions,
                                        colour=mod_colour,
                                        mentionable=True,
                                        hoist=True,
                                        reason=role_reason)
        if "guildmates" not in current_roles:
            await ctx.guild.create_role(name="guildmates",
                                        permissions=guildmate_permissions,
                                        colour=guildmate_colour,
                                        mentionable=True,
                                        hoist=True,
                                        reason=role_reason)
        if "lurkers" not in current_roles:
            await ctx.guild.create_role(name="lurkers",
                                        permissions=lurker_permissions,
                                        colour=lurker_colour,
                                        mentionable=True,
                                        hoist=True,
                                        reason=role_reason)
        if "nsfw" not in current_roles:
            await ctx.guild.create_role(name="nsfw",
                                        permissions=unverified_permissions,
                                        color=unverified_colour,
                                        mentionable=False,
                                        hoist=False,
                                        reason=role_reason)
        if "unverified" not in current_roles:
            await ctx.guild.create_role(name="unverified",
                                        permissions=unverified_permissions,
                                        colour=unverified_colour,
                                        mentionable=True,
                                        hoist=True,
                                        reason=role_reason)

        await ctx.send("Roles created!")

    @commands.command()
    async def nsfw(self, ctx):
        """
        Adds the nsfw role to a user. This would allow them to view the nsfw
        channel.
        """
        # This assumes that the guild has one, and only one, role named nsfw
        nsfw_role = ctx.guild.roles
        nsfw_role = [role for role in nsfw_role if role.name == "nsfw"]
        nsfw_role = nsfw_role[0]
        await ctx.author.add_roles(nsfw_role)


def setup(bot):
    bot.add_cog(GuildManager(bot))
