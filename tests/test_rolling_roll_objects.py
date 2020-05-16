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


class TestDndRoll(unittest.TestCase):
    def setUp(self):
        self.parser = parsers.DndRollParser()

    def test_initialization(self):
        roll = ["1", "+2", "-adv", "-n", "Hello", "world"]
        roll = self.parser.parse_args(roll)
        roll = rolls.DndRoll(roll)
        run(roll.roll())

        self.assertEqual(len(roll.result), 1)
        self.assertEqual(roll.note, ["Hello", "world"])

    def test_adv_format(self):
        """Ensures advantage roll formatting works"""
        roll = ["1", "+2", "-adv", "-n", "Hello", "world"]
        roll = self.parser.parse_args(roll)
        roll = rolls.DndRoll(roll)
        roll = run(roll.format())

        self.assertTrue("Advantage" in roll)

    def test_dis_format(self):
        """Ensures disadvantage roll formatting works"""
        roll = ["1", "+2", "-dis", "-n", "Hello", "world"]
        roll = self.parser.parse_args(roll)
        roll = rolls.DndRoll(roll)
        roll = run(roll.format())

        self.assertTrue("Disadvantage" in roll)

    def test_general_format(self):
        """Ensures general roll formatting works"""
        roll = ["1", "+2", "-n", "Hello", "world"]
        roll = self.parser.parse_args(roll)
        roll = rolls.DndRoll(roll)
        roll = run(roll.format())

        self.assertFalse("Disadvantage" in roll)
        self.assertFalse("Advantage" in roll)


class TestSr3Roll(unittest.TestCase):
    def setUp(self):
        self.parser = parsers.Sr3RollParser()

    def test_initialization(self):
        roll = ["6", "5", "-n", "hello", "world"]
        roll = self.parser.parse_args(roll)
        roll = rolls.Sr3Roll(roll)
        run(roll.roll())

        self.assertEqual(roll.threshold, 5)
        self.assertEqual(roll.dice, 6)
        self.assertEqual(roll.note, ["hello", "world"])

    def test_format(self):
        """Ensures format returns a string"""
        roll = ["6", "5", "-n", "hello", "world"]
        roll = self.parser.parse_args(roll)
        roll = rolls.Sr3Roll(roll)
        roll = run(roll.format())
        self.assertTrue(isinstance(roll, str))
        self.assertTrue("Initiative" not in roll)

    def test_initiative_format(self):
        """Ensures that "Initiative" appears in formatted string when an
        initiative roll is made"""
        roll = self.parser.parse_args(["6", "-i", "10"])
        roll = rolls.Sr3Roll(roll)
        roll = run(roll.format())
        self.assertTrue("Initiative" in roll)
        self.assertTrue("Hits" not in roll)

    def test_open_ended_format(self):
        """Ensures that "Open" is in the formatted string"""
        roll = self.parser.parse_args(["6", "-o"])
        roll = rolls.Sr3Roll(roll)
        roll = run(roll.format())
        self.assertTrue("Open" in roll)
        self.assertTrue("Hits" not in roll)


def run(coroutine):
    """
    Runs and returns the data from the couroutine passed in. This is to
    only be used in unittesting.

    coroutine : asyncio coroutine

        -> coroutine return
    """

    return asyncio.get_event_loop().run_until_complete(coroutine)
