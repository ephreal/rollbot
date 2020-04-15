# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

from discord import Colour, Embed


async def embed_reply(author, content, color=Colour.blue()):
    """
    Creates the embedded message to send to discord

    author: discord.Member
    content: str
    color: discord.Colour

        -> discord.Embed
    """

    message = Embed()
    message.set_author(name=author.name, icon_url=author.avatar_url)
    message.thumbnail.height = 128
    message.thumbnail.width = 128
    message.description = content
    message.colour = color

    return message
