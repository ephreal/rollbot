# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

import argparse


class InvalidArgumentsError(Exception):
    """Raise an InvalidArgumentsError instead of exiting the program"""
    pass


class BaseRollParser(argparse.ArgumentParser):
    """
    A roll parser that handles basic dice rolling.
    """
    def __init__(self):
        super().__init__()
        self.add_argument('dice', metavar="XdY", default="", nargs="?",
                          help="dice, in XdY format")
        self.add_argument('-m', "--mod", type=int, default=0,
                          help="modifier to add to final result")
        self.add_argument('-n', '--note', nargs="*",
                          help="Note about this roll")

    def error(self, message):
        raise InvalidArgumentsError


class Sr1RollParser(BaseRollParser):
    """
    A roll parser for shadowrun.
    """

    def __init__(self):
        super().__init__()
        # Currently nothing else required for SR1E beyond the base roller. I
        # have yet to read through the docs to get this sorted.


class Sr5RollParser(BaseRollParser):
    """
    A roll parser for shadowrun.
    """

    def __init__(self):
        super().__init__()
        self.add_argument('-ext', '--extended', action='store_true')
