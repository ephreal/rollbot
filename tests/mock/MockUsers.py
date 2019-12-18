# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""


class DiscordUser():
    """
    Mock user to test the discord interface with

    Class Variables
        id (int):
            represents the member.id from discord.member

    Class Methods
        send(message: str) -> None:
            Creates a file in the same folder with the name "player_message"
            that conatins the message. The message can then be verified.
    """

    def __init__(self, userid=None, name=None):
        self.id = userid
        self.name = name

    async def send(self, message):
        """
        Creates a file in the same folder with the name "player_message" that
        conatins the message. The message can then be verified.

        mesasge: str
            -> None
        """

        with open("player_message", "w") as f:
            f.write(message)
