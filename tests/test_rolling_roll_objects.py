# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""


import asyncio
import unittest
from utils.rolling import rolls
from utils.rolling import parsers


class TestBaseRoll(unittest.TestCase):
    def setUp(self):
        self.parser = parsers.BaseRollParser()

    def test_initialization(self):
        """
        Verifies that the roll is initialized properly and has no issues.
        """

        roll = ["3d6"]
        roll = self.parser.parse_args(roll)
        roll = rolls.BaseRoll(roll)
        self.assertEqual(roll.dice, 3)
        self.assertEqual(roll.sides, 6)

        roll = ["-m", "6", "6d10", "-n", "This", "is", "a", "test"]
        roll = self.parser.parse_args(roll)
        roll = rolls.BaseRoll(roll)
        self.assertEqual(roll.dice, 6)
        self.assertEqual(roll.sides, 10)
        self.assertEqual(roll.mod, 6)
        self.assertEqual(roll.note, ["This", "is", "a", "test"])

    def test_format(self):
        """
        Verifies the roll is able to format rolls properly
        """

        roll = ["3d6", "-n", "test"]
        roll = self.parser.parse_args(roll)
        roll = rolls.BaseRoll(roll)
        roll = run(roll.format())
        self.assertTrue(isinstance(roll, str))


def run(coroutine):
    """
    Runs and returns the data from the couroutine passed in. This is to
    only be used in unittesting.

    coroutine : asyncio coroutine

        -> coroutine return
    """

    return asyncio.get_event_loop().run_until_complete(coroutine)
