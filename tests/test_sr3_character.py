# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""


import asyncio
import unittest
from utils.rolling.handlers import Sr3RollHandler
from utils.rpg.shadowrun3e import character


attributes = {
    "name": "Glen",
    "age": 44,
    "plazzate": "EEssdDEd",
    "attributes": {
        "strength": {
            "base": 9001,
            "modifier": 0
        }
    },
    "skills": {
        "athletics": {
            "level": 4,
        }
    }
}


class TestSR3Character(unittest.TestCase):
    def setUp(self):
        self.character = character.SR3Character(**attributes)

    def test_initialization(self):
        """Ensures the character can initialize properly"""
        self.assertEqual(self.character.name, "Glen")
        with self.assertRaises(AttributeError):
            self.character.plazzate

    def test_to_json(self):
        """Ensures that to_dict returns a valid dict."""
        char_dict = run(self.character.to_dict())
        self.assertEqual(char_dict["age"], 44)
        attribute = char_dict["attributes"]["strength"]
        self.assertEqual(attribute['base'], 9001)

    def test_get_attribute(self):
        attribute = run(self.character.get_attribute("strength"))
        self.assertEqual(attribute["base"], 9001)

    def test_roll_handler(self):
        """
        Ensures the roll handler is present and of the correct type.
        """
        self.assertTrue(isinstance(self.character.handler, Sr3RollHandler))

    def test_roll_attribute(self):
        """
        Ensures the character is able to roll with attributes
        """
        ridiculous_roll = run(self.character.roll_attribute("strength", 4))
        self.assertTrue(ridiculous_roll.dice, 9001)

    def test_roll_skill(self):
        """
        Ensures the character is able to roll with skills
        """

        skill_roll = run(self.character.roll_skill("athletics", 4))
        self.assertEqual(skill_roll.dice, 4)

    def test_roll_spell(self):
        """
        Verifies that roll_spell rolls the spell pool for now
        """

        self.character.skills['sorcery'] = 6
        spell_roll = run(self.character.roll_skill('sorcery'))
        self.assertEqual(spell_roll.dice, 6)


def run(coroutine):
    """
    Runs and returns the data from the couroutine passed in. This is to
    only be used in unittesting.

    coroutine : asyncio coroutine

        -> coroutine return
    """

    return asyncio.get_event_loop().run_until_complete(coroutine)
