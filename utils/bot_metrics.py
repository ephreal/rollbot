# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

from datetime import datetime
from utils import message_builder


async def format_all_usage(commands):
    """
    Formats the output of utils.handlers.MetricsDB.get_all_usage

    commands: list[[name, usage], [name, usage] .....]
        -> usage: list[discord.Embed()]
    """

    messages = []
    replies = []
    embed = []
    total_len = 0

    for command in commands:
        message = []
        message.append(f"{command[0]}: {command[1]}")
        message.append(len(f"{command[0]}: {command[1]}"))
        messages.append(message)

    for message in messages:
        if (total_len + message[1]) > 2000:
            reply = message_builder.embed_reply_no_author("\n".join(replies))
            total_len = 0
            replies = []
            embed.append(reply)

        replies.append(message[0])
        total_len += message[1]

    reply = message_builder.embed_reply_no_author("\n".join(replies))
    embed.append(reply)

    return embed


async def uptime_calculation(bot, curr_time=None):
    """
    Calculates the uptime based on the passed in bot boot time and the current
    time passed in. Current time is remaining passed in to assist with testing
    of the code.

    bot: discord.ext.commands.Bot()
    curr_time: datetime.now()
        -> uptime: string
    """
    if not curr_time:
        curr_time = datetime.now()

    difference = curr_time - bot.boot_time
    days = difference.days
    difference = difference.seconds

    difference %= 86400

    hours = difference // 3600
    difference %= 3600

    minutes = difference // 60
    seconds = difference % 60

    message = f"The bot has been up for {days} days, " \
              f"{hours} hours, {minutes} minutes, and {seconds} seconds"

    return message
