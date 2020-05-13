# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

import unittest
from utils.rolling import parsers


class TestBaseRoller(unittest.TestCase):
    def setUp(self):
        self.parser = parsers.BaseRollParser()

    def test_dice_parsing(self):
        """
        Ensures the roll parser is able to find the dice correctly
        """

        roll = ["6d10"]
        roll = self.parser.parse_args(roll)

        self.assertEqual(roll.dice, "6d10")

    def test_modifier_handling(self):
        roll = ["6d10", "-m", "+5"]
        roll = self.parser.parse_args(roll)

        self.assertEqual(roll.dice, "6d10")
        self.assertEqual(roll.mod, 5)

        roll = ["-m", "-5", "6d10"]
        roll = self.parser.parse_args(roll)
        self.assertEqual(roll.mod, -5)

    def test_note_handling(self):
        roll = ["6d10", "-n", "Roll for initiative"]
        roll = self.parser.parse_args(roll)

        self.assertEqual(roll.note[0], "Roll for initiative")


class TestSr1Roller(unittest.TestCase):
    def setUp(self):
        self.parser = parsers.Sr1RollParser()
    # Nothing to test on this yet


class TestSr5Roller(unittest.TestCase):
    def setUp(self):
        self.parser = parsers.Sr5RollParser()

    def test_extended_flag(self):
        roll = self.parser.parse_args([])
        self.assertFalse(roll.extended)

        roll = self.parser.parse_args(["-ex"])
        self.assertTrue(roll.extended)
