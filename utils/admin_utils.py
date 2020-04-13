# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

import random


async def shutdown_message():
    shutdown_message = "The bot is currently shutting down. Good bye"
    shutdown_message = shutdown_message[0:random.randint(0,
                                        len(shutdown_message)-1)]
    return shutdown_message


async def write_shutdown_file():
    with open("poweroff", "w") as f:
        f.write("Poweroff the bot.")
