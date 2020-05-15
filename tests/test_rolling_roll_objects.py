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
        self.parser = parsers.BasicRollParser()

    def test_initialization(self):
        """
        Verifies that the roll is initialized properly and has no issues.
        """

        roll = ["3d6"]
        roll = self.parser.parse_args(roll)
        roll = rolls.BaseRoll(roll)
        self.assertEqual(roll.dice, 3)
        self.assertEqual(roll.sides, 6)

        roll = ["6d10", "6", "-n", "This", "is", "a", "test"]
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


class TestSr1Roll(unittest.TestCase):
    def setUp(self):
        self.parser = parsers.Sr1RollParser()

    def test_initialization(self):
        roll = ["6", "5", "-n", "hello", "world"]
        roll = self.parser.parse_args(roll)
        roll = rolls.Sr1Roll(roll)
        run(roll.roll())

        self.assertEqual(roll.threshold, 5)
        self.assertEqual(roll.dice, 6)
        self.assertEqual(roll.note, ["hello", "world"])

    def test_format(self):
        """Ensures format returns a string"""
        roll = ["6", "5", "-n", "hello", "world"]
        roll = self.parser.parse_args(roll)
        roll = rolls.Sr1Roll(roll)
        roll = run(roll.format())
        self.assertTrue(isinstance(roll, str))
        self.assertTrue("Initiative" not in roll)

    def test_initiative_format(self):
        """Ensures that "Initiative" appears in formatted string when an
        initiative roll is made"""
        roll = self.parser.parse_args(["6", "-i", "10"])
        roll = rolls.Sr1Roll(roll)
        roll = run(roll.format())
        self.assertTrue("Initiative" in roll)
        self.assertTrue("Hits" not in roll)


def run(coroutine):
    """
    Runs and returns the data from the couroutine passed in. This is to
    only be used in unittesting.

    coroutine : asyncio coroutine

        -> coroutine return
    """

    return asyncio.get_event_loop().run_until_complete(coroutine)
