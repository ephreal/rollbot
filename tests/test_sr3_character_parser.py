# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""


import unittest
from utils.rpg.shadowrun3e.parser import Sr3CharacterParser


class TestSr3eCharacterParser(unittest.TestCase):
    def setUp(self):
        self.parser = Sr3CharacterParser

    def test_roll_attribute_parse(self):
        """
        Verifies that the attribute roll parsing works properly
        """
        to_parse = ["roll", "4", "-a", "strength"]
        parsed = self.parser.parse_args(to_parse)
        self.assertEqual(parsed.attribute, "strength")
        self.assertEqual(parsed.threshold, "4")
        self.assertFalse(parsed.skill)
        self.assertFalse(parsed.spell)

    def test_roll_skill_parse(self):
        """
        Verifies that the skill roll parsing works properly
        """
        to_parse = ["roll", "6", "-sk", "athletics"]
        parsed = self.parser.parse_args(to_parse)
        self.assertEqual(parsed.skill, "athletics")
        self.assertEqual(parsed.threshold, "6")
        self.assertFalse(parsed.attribute)
        self.assertFalse(parsed.spell)

    def test_roll_spell_parse(self):
        """
        Verifies that the spell roll parsing works properly
        """
        to_parse = ["roll", "5", "-sp", "fireball"]
        parsed = self.parser.parse_args(to_parse)
        self.assertEqual(parsed.spell, "fireball")
        self.assertEqual(parsed.threshold, "5")
        self.assertFalse(parsed.skill)
        self.assertFalse(parsed.attribute)

    def test_view_attributes(self):
        """
        Verifies that the attribute viewing works as expected
        """

        attribute = ["attr"]
        attribute = self.parser.parse_args(attribute)
        self.assertFalse(attribute.attribute)

        attribute = ["attr", "strength", "-m" "6"]
        attribute = self.parser.parse_args(attribute)
        self.assertEqual(attribute.attribute, "strength")
        self.assertEqual(attribute.modify, "6")

    def test_view_skills(self):
        """
        Verifies that the skill viewing works as expected
        """

        skill = ["skill"]
        skill = self.parser.parse_args(skill)
        self.assertFalse(skill.skill)

        skill = ["skill", "athletics", "-a"]
        skill = self.parser.parse_args(skill)
        self.assertEqual(skill.skill, "athletics")
        self.assertTrue(skill.add, True)

    def test_view_spells(self):
        """
        Verifies that spell viewing works
        """
        spell = ["spell"]
        spell = self.parser.parse_args(spell)
        self.assertFalse(spell.spell)

        spell = ["spell", "fireball", "-a"]
        spell = self.parser.parse_args(spell)
        self.assertEqual(spell.spell, "fireball")
        self.assertTrue(spell.add)
