# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

import logging
import os
import random


async def shutdown_message():
    shutdown_message = "The bot is currently shutting down. Good bye"
    shutdown_message = shutdown_message[0:random.randint(0,
                                        len(shutdown_message)-1)]
    return shutdown_message


async def write_shutdown_file():
    with open("poweroff", "w") as f:
        f.write("Poweroff the bot.")


def setup_logging(bot, logfile="discord.log"):
    """
    Called from the __init__ method of the admin cog, therefore this cannot
    be and async method.

    Setup logging and log file

    bot: discord.ext.command.Bot
    """

    # Rotate log files
    if os.path.exists(f"{logfile}.bak"):
        os.remove(f"{logfile}.bak")

    if os.path.exists(logfile):
        os.rename(logfile, f"{logfile}.bak")

    bot.logger = logging.getLogger('discord')
    bot.logger.setLevel(logging.CRITICAL)
    bot.handler = logging.FileHandler(filename=logfile,
                                      encoding='utf-8', mode='w')
    bot.handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:'
                                               '%(name)s: %(message)s'))
    bot.logger.addHandler(bot.handler)


async def change_log_level(bot, log_level):
    """
    Change the log level. Available logging levels are
        CRITICAL
        ERROR
        WARNING
        INFO
        DEBUG
    DEBUG is the most verbose, CRITICAL is the least verbose

    bot: discord.ext.commands.Bot
    log_level: string
    """

    bot.logger.setLevel(log_level)
