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
    message.set_author(name=author.name, icon_url=author.avatar)
    message.thumbnail.height = 128
    message.thumbnail.width = 128
    message.description = content
    message.colour = color

    return message


def embed_reply_no_author(content, color=Colour.blue()):
    """
    Embedded reply for when no author is required. For example, showing command
    usage.
    """
    message = Embed()
    message.description = content
    message.colour = color
    return message


async def embed_catapi_image(ctx, image):

    author = ctx.author
    message = Embed()
    breed = ""
    if image.breed:
        breed = f"breed: {breed.name}    breed_id: {breed.id}\n"
        message.footer = breed.wikipedia_url

    message.set_author(name=author.name, icon_url=author.avatar)
    message.colour = Colour.green()
    message.description = f"Image id: {image.id}\n{breed}{image.url}"
    message.set_image(url=image.url)
    return message


async def on_join_builder(member, message=None):
    """
    Returns a message to send to the member who joined the server

    member: discord.Member
        -> welcome_message: discord.Embed
    """

    welcome_message = Embed(title=f"Welcome to {member.guild.name}!")

    if not message:
        message = f"Welcome to {member.guild.name}! Please remember to be"\
                  " kind and courteous. If you would like to join in " \
                  "bot testing, please run '.bottester' to have the role "\
                  "assigned to you."
    else:
        footer = "Note: This message was not created by the bot author.\n" \
                 "If you find it offensive, contact the moderation team for "\
                 f"{member.guild.name}"
        welcome_message.set_footer(text=footer)

    welcome_message.colour = Colour.green()
    welcome_message.set_thumbnail(url=member.guild.icon_url)
    welcome_message.thumbnail.height = 128
    welcome_message.thumbnail.width = 128
    welcome_message.description = message

    return welcome_message
