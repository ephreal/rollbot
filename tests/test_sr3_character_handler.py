# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""


from utils.rpg.shadowrun3e.handler import SR3CharacterHandler
from utils.rpg.shadowrun3e.character import SR3Character
import asyncio
import unittest
import json


class TestSR3eCharacterHandler(unittest.TestCase):
    def setUp(self):
        with open('tests/mock/sr3_character.json', 'r') as f:
            character = json.loads(f.read())
        self.character = SR3Character(**character)
        self.handler = SR3CharacterHandler(self.character)

    def test_roll_attribute(self):
        """
        Verifies that a valid roll object gets returned
        """
        roll = ["roll", "4", "-a", "strength", "-n", "test roll"]
        roll = run(self.handler.parse(roll))
        roll = run(self.handler.roll_attribute(roll))
        self.assertTrue(roll)
        self.assertEqual(roll.note, ["test roll"])

    def test_roll_skill(self):
        """
        Verifies that a valid roll object is returned
        """
        roll = ["roll", "4", "-sk", "rifles", "-n", "skill", "roll"]
        roll = run(self.handler.parse(roll))
        roll = run(self.handler.roll_skill(roll))
        self.assertTrue(roll)
        self.assertEqual(roll.note, ["skill", "roll"])
        self.assertEqual(roll.dice, 6)

        # Test that specializations roll properly
        roll = ["roll", "4", "-sk", "ak47", "-n", "specialization", "roll"]
        roll = run(self.handler.parse(roll))
        roll = run(self.handler.roll_skill(roll))
        self.assertTrue(roll)
        self.assertEqual(roll.dice, 8)

    def test_modify_attribute(self):
        """
        Verifies that modifying an attribute works as expected
        """
        current = self.character.attributes['strength']['base']
        attr = ['attr', 'str', '1']
        attr = run(self.handler.parse(attr))
        attr = run(self.handler.modify_attribute(attr))
        self.assertEqual(attr['base'], current+1)
        char_strength = self.handler.character.attributes['strength']
        self.assertEqual(char_strength['base'], current+1)

    def test_override_attribute(self):
        """
        Verifies that overriding an attribute works as expected
        """
        attr = ['attr', 'q', '-o', '10']
        attr = run(self.handler.parse(attr))
        attr = run(self.handler.override_attribute(attr))
        self.assertEqual(attr['override'], 10)
        char_quick = self.handler.character.attributes['quickness']
        self.assertEqual(char_quick['override'], 10)

    def test_modify_karma(self):
        """
        Verifies that the karma modifies properly
        """
        karma = run(self.handler.parse(["karma", "6"]))
        karma = run(self.handler.modify_karma(karma))
        self.assertEqual(karma['good'], 10)
        self.assertEqual(karma['total'], 10)
        self.assertEqual(karma['pool'], 1)

    def test_handle_args_roll_parsing(self):
        """
        Verifies that the args handler hands off to the roll parser properly
        """
        roll = ['roll', '6', '-a', 'str']
        roll = run(self.handler.handle_args(roll))
        self.assertEqual(roll.threshold, '6')
        self.assertEqual(roll.dice, 6)

        roll = ['roll', '3', '-sk', 'rifles']
        roll = run(self.handler.handle_args(roll))
        self.assertEqual(roll.threshold, '3')
        self.assertEqual(roll.dice, 6)

    def test_handler_args_attr_parsing(self):
        """
        Ensures the args handler hands off to the attribute parser
        """

        attr = ['attr', 'str', '1', '-n', 'str', 'testing']
        attr = run(self.handler.handle_args(attr))
        self.assertEqual(6, attr['base'])

        attr = ['attr', 'body', '-o', '7']
        self.assertEqual(self.character.attributes['body']['override'], 0)
        attr = run(self.handler.handle_args(attr))
        self.assertEqual(self.character.attributes['body']['override'], 7)

        attr = ['attr', 'quick', '-m' '10']
        current = self.character.attributes['quickness']['modifier']
        self.assertEqual(current, 0)
        attr = run(self.handler.handle_args(attr))
        self.assertEqual(attr['modifier'], 10)
        current = self.character.attributes['quickness']['modifier']
        self.assertEqual(current, 10)

        attr = ["attr", "int", '4', '-s']
        attr = run(self.handler.handle_args(attr))
        self.assertEqual(attr['base'], 4)

    def test_handler_args_skill_parsing(self):
        """
        Ensures the args handler hands off to the skill parser.
        """
        skill = ["skill", "pistols", "-a"]
        skill = run(self.handler.handle_args(skill))
        self.assertEqual(skill['level'], 1)
        self.assertTrue(self.character.skills['pistols'])
        karma = self.character.karma['good']
        self.assertEqual(karma, 3)

        skill = ['skill', 'pistols', '1', '-m']
        skill = run(self.handler.handle_args(skill))
        self.assertEqual(skill['level'], 2)
        pistols = self.character.skills['pistols']
        self.assertEqual(pistols['level'], 2)


def run(coroutine):
    """
    Runs and returns the data from the couroutine passed in. This is to
    only be used in unittesting.

    coroutine : asyncio coroutine

        -> coroutine return
    """

    return asyncio.get_event_loop().run_until_complete(coroutine)
