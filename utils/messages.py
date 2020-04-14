# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

from discord import Colour, Embed


def endorse(bot_nick):
    """
    Returns a silly message to reply to messages with.

    bot_nick: str
        -> endorsement: str
    """

    endorsement = f"My name is {bot_nick}, and I endorse the above message.\n"\
                  "Note that my endorsement in no way reflects the opinions " \
                  "of me or my creator, does not make any guarantee about the"\
                  " correctness of said message, and may, in fact, not be an "\
                  "actual endorsement of the sentiments expressed in said "\
                  "message."
    return endorsement


def on_join_message(member):
    """
    Returns a message to send to the member who joined the server

    member: discord.Member
        -> welcome_message: discord.Embed
    """

    on_join_message = f"Welcome to {member.guild.name}! Please remember to be"\
                      " kind and courteous. If you would like to join in " \
                      "bot testing, please run '.bottester' to have the role "\
                      "assigned to you."

    welcome_message = Embed(title=f"Welcome to {member.guild.name}!")
    welcome_message.colour = Colour.green()
    welcome_message.set_thumbnail(url=member.guild.icon_url)
    welcome_message.thumbnail.height = 128
    welcome_message.thumbnail.width = 128
    welcome_message.description = on_join_message

    return welcome_message
