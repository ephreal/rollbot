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
        self.parser = parsers.BasicRollParser()
        self.roll_type = rolls.BaseRoll

    async def parse(self, args):
        return self.parser.parse_args(args)

    async def roll(self, args):
        """
        args: [roll_arguments]
            -> roll: Result
        """
        roll = self.parser.parse_args(args)
        roll = self.roll_type(roll)
        await roll.roll()

        return roll


class DndRollHandler(BaseRollHandler):
    def __init__(self):
        self.parser = parsers.DndRollParser()
        self.roll_type = rolls.DndRoll


class Sr3RollHandler(BaseRollHandler):
    def __init__(self):
        self.parser = parsers.Sr3RollParser()
        self.roll_type = rolls.Sr3Roll
