# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""


from utils.rolling import parsers
from utils.rolling import rolls


class BaseRollHandler():
    """
    Base roll handler class for all other roll handlers.

    note: This does not obsolete any other base roll handlers yet, but it will
           in the future

    Methods
    -------

    parse(args)
    roll(args)
    """

    def __init__(self):
        self.parser = parsers.BaseRollParser()

    async def parse(self, args):
        return self.parser.parse_args(args)

    async def roll(self, args):
        """
        args: [roll_arguments]
            -> roll: Result
        """
        roll = self.parser.parse_args(args)
        roll = rolls.BaseRoll(roll)
        await roll.roll()

        return roll
