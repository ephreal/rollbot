# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

import argparse


class ArgumentParserError():
    pass


class BotParser(argparse.ArgumentParser):
    """
    A bot-safe version of argparse. AKA: It won't shut the bot off when if it
    has errors parsing things.
    """
    def __init__(self):
        super().__init__()

    def error(self, message):
        """
        I'd like to print out the message for the user and NOT cause the bot
        to exit, so trhowing an exception with the message here.
        """
        raise ArgumentParserError(message)


class BaseRollParser(BotParser):
    """
    Argument parser for basic rolling

    First checks to see anything matching "xDy" exists in the string.
    """
    def __init__(self):
        super().__init__()
        self.add_argument('-r', nargs="*", help="Roll XdY dice",
                          action="append")
