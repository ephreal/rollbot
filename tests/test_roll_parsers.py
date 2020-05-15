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

    def test_note_handling(self):
        roll = ["6d10", "-n", "Roll for initiative"]
        roll = self.parser.parse_args(roll)

        self.assertEqual(roll.note[0], "Roll for initiative")


class TestBasicRollParser(unittest.TestCase):
    def setUp(self):
        self.parser = parsers.BasicRollParser()

    def test_modifier_handling(self):
        roll = ["6d10", "+5"]
        roll = self.parser.parse_args(roll)

        self.assertEqual(roll.dice, "6d10")
        self.assertEqual(roll.mod, 5)


class TestSr1Roller(unittest.TestCase):
    def setUp(self):
        self.parser = parsers.Sr1RollParser()

    def test_thresholds(self):
        """
        Ensures that thresholds are able to be captured properly
        """

        roll = self.parser.parse_args(["6", "7"])
        self.assertEqual(roll.threshold, 7)
        self.assertEqual(roll.dice, "6")

    def test_initiative(self):
        """
        Ensures that initiative modifiers can be added properly
        """

        roll = self.parser.parse_args(["6", "7", "-i", "12"])
        self.assertEqual(roll.initiative, 12)


class TestSr5Roller(unittest.TestCase):
    def setUp(self):
        self.parser = parsers.Sr5RollParser()

    def test_extended_flag(self):
        roll = self.parser.parse_args([])
        self.assertFalse(roll.extended)

        roll = self.parser.parse_args(["-ex"])
        self.assertTrue(roll.extended)
