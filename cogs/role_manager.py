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


Commands provided by this cog:

    create_roles : Creates the roles for the bot's member promotion command
"""


from discord.ext import commands
from discord import Colour
from discord import Permissions


class RoleManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Setup roles for bot")
    @commands.has_permissions(manage_roles=True)
    async def create_roles(self, ctx):
        if not ctx.guild.me.guild_permissions.manage_roles:
            return await ctx.send("I need the manage roles permission.")

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

        await ctx.guild.create_role(name="admins",
                                    permissions=admin_permissions,
                                    colour=admin_colour,
                                    mentionable=True,
                                    hoist=True)
        await ctx.guild.create_role(name="mods",
                                    permissions=mod_permissions,
                                    colour=mod_colour,
                                    mentionable=True,
                                    hoist=True)
        await ctx.guild.create_role(name="guildmates",
                                    permissions=guildmate_permissions,
                                    colour=guildmate_colour,
                                    mentionable=True,
                                    hoist=True)
        await ctx.guild.create_role(name="lurkers",
                                    permissions=lurker_permissions,
                                    colour=lurker_colour,
                                    mentionable=True,
                                    hoist=True)
        await ctx.guild.create_role(name="unverified",
                                    permissions=unverified_permissions,
                                    colour=unverified_colour,
                                    mentionable=True,
                                    hoist=True)

        await ctx.send("Roles created!")


def setup(bot):
    bot.add_cog(RoleManager(bot))
