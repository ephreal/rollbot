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

import json
import os
import datetime


class GuildAnalytics():
    def __init__(self):
        if os.path.exists("analytics/stats.json"):
            with open("analytics/stats.json", "r") as f:
                self.analytics = json.load(f)
        else:
            os.mkdir("analytics")
            self.analytics = {}

    def add_guild(self, ctx):
        """
        Adds a guild to the analytics. This allows the bot to track how often
        users send messages, if users are sending messages at all, etc. This
        way it's easy to tell which users may be dormant on an old server.
        """

        self.analytics[ctx.guild.id] = {
            "name": ctx.message.guild.name,
            "guild_owner": ctx.guild.owner,
            "members": self.format_members(ctx.guild.members),
            "stale_members": None,
            "channels": self.format_channels(ctx.guild.channels),
        }

    def format_members(self, members):
        """
        Formats members in the guild in a manner that analytics can use.
        """

        now = datetime.datetime.now()

        formatted_members = {}

        for member in members:
            formatted_members[member.name] = {
                "joined_at": member.joined_at,
                "nickname": member.nick,
                "guilds": member.guild,
                "last_message": now,
                "last_typing": now,
                "last_typing_channel": None,
                "last_voice": now,
                "last_voice_channel": None,
                "last_online": now,
                "roles": member.roles,
                "top_role": member.top_role,
                "permissions": member.guild_permissions,
            }

            return formatted_members

    def format_channels(self, channels):
        """
        Formats channels in the guild to the analytics can be used.
        """

        formatted_channels = {}

        for channel in channels:
            formatted_channels[channel.id] = {
                "name": channel.name,
                "type": channel.type,
            }

        return formatted_channels
