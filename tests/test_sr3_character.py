# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""


import asyncio
import json
import unittest
from utils.rpg.shadowrun3e import character


class TestSR3Character(unittest.TestCase):
    def setUp(self):
        with open('tests/mock/sr3_character.json', 'r') as f:
            srcharacter = json.loads(f.read())
        self.character = character.SR3Character(**srcharacter)

    def test_initialization(self):
        """Ensures the character can initialize properly"""
        self.assertEqual(self.character.name, "Fred")
        with self.assertRaises(AttributeError):
            self.character.plazzate

    def test_to_json(self):
        """Ensures that to_dict returns a valid dict."""
        char_dict = run(self.character.to_dict())
        self.assertEqual(char_dict["age"], 19)
        attribute = char_dict["attributes"]["strength"]
        self.assertEqual(attribute['base'], 5)

    def test_get_attribute(self):
        attribute = run(self.character.get_attribute("strength"))
        self.assertEqual(attribute["base"], 5)

    def test_modify_karma(self):
        """
        Ensures that modifying karma is done sanely
        """

        run(self.character.modify_karma(-1))
        self.assertEqual(self.character.karma, 4)
        self.assertEqual(self.character.career['karma'], 5)

        run(self.character.modify_karma(5))
        self.assertEqual(self.character.karma, 9)
        self.assertEqual(self.character.career['karma'], 10)

    def test_set_attribute_modifier(self):
        """
        Ensures the attribute modifier is set properly
        """

        run(self.character.set_attribute_modifier('charisma', 9))
        modifier = self.character.attributes['charisma']['modifier']
        self.assertEqual(modifier, 9)

    def test_modify_physical_condition(self):
        """
        Verifies the physical condition is handled sanely
        """

        condition = run(self.character.modify_physical_condition(5))
        self.assertEqual(condition['physical'], 5)

        condition = run(self.character.modify_physical_condition(7))
        self.assertEqual(condition['physical'], 10)
        self.assertEqual(condition['overflow'], 2)

        condition = run(self.character.modify_physical_condition(-3))
        self.assertEqual(condition['physical'], 9)
        self.assertEqual(condition['overflow'], 0)

        condition = run(self.character.modify_physical_condition(-10))
        self.assertEqual(condition['physical'], 0)

    def test_modify_stun_condition(self):
        """
        Verifies that stun condition is handled properly
        """

        condition = run(self.character.modify_stun_condition(5))
        self.assertEqual(condition['stun'], 5)

        condition = run(self.character.modify_stun_condition(7))
        self.assertEqual(condition['stun'], 10)
        self.assertEqual(condition['physical'], 2)

        condition = run(self.character.modify_stun_condition(9))
        self.assertEqual(condition['stun'], 10)
        self.assertEqual(condition['physical'], 10)
        self.assertEqual(condition['overflow'], 1)


def run(coroutine):
    """
    Runs and returns the data from the couroutine passed in. This is to
    only be used in unittesting.

    coroutine : asyncio coroutine

        -> coroutine return
    """

    return asyncio.get_event_loop().run_until_complete(coroutine)
