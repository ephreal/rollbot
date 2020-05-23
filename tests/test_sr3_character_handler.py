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

character = {"name": "fred",
             "attributes": {
                "strength": {
                    "base": 5,
                    "override": 0,
                    "modifier": 1},
                "quickness": {
                    "base": 6,
                    "override": 0,
                    "modifier": 0
                    },
                    },
             "skills": {
                    "rifles": {
                        "attribute": "Quickness",
                        "build_repair": True,
                        "category": "combat",
                        "defaults": "Assault Rifles, Pistols, Shotguns",
                        "description": "Sport and Sniper Rifles",
                        "source": "SR3E Core p. 86",
                        "specializations": {
                            "ak47": {
                                "level": 8
                            }
                        },
                        "level": 6
                    },
                }
             }


class TestSR3eCharacterHandler(unittest.TestCase):
    def setUp(self):
        self.character = SR3Character(**character)
        self.handler = SR3CharacterHandler(self.character)

    def test_roll_attribute(self):
        """
        Verifies that a valid roll object gets returned
        """
        roll = ["roll", "4", "-a", "strength", "-n", "test roll"]
        roll = run(self.handler.roll_attribute(roll))
        self.assertTrue(roll)
        self.assertEqual(roll.note, ["test roll"])

    def test_roll_skill(self):
        """
        Verifies that a valid roll object is returned
        """
        roll = ["roll", "4", "-sk", "rifles", "-n", "skill", "roll"]
        roll = run(self.handler.roll_skill(roll))
        self.assertTrue(roll)
        self.assertEqual(roll.note, ["skill", "roll"])
        self.assertEqual(roll.dice, 6)

        # Test that specializations roll properly
        roll = ["roll", "4", "-sk", "ak47", "-n", "specialization", "roll"]
        roll = run(self.handler.roll_skill(roll))
        self.assertTrue(roll)
        self.assertEqual(roll.dice, 8)


def run(coroutine):
    """
    Runs and returns the data from the couroutine passed in. This is to
    only be used in unittesting.

    coroutine : asyncio coroutine

        -> coroutine return
    """

    return asyncio.get_event_loop().run_until_complete(coroutine)
