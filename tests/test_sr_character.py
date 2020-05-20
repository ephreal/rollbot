# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""


import asyncio
import unittest
from utils.rpg.shadowrun3e import character


attributes = {
    "name": "Glen",
    "age": 44,
    "plazzate": "EEssdDEd",
    "attributes": {
        "strength": 9001
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
        self.assertEqual(char_dict["attributes"]["strength"], 9001)


def run(coroutine):
    """
    Runs and returns the data from the couroutine passed in. This is to
    only be used in unittesting.

    coroutine : asyncio coroutine

        -> coroutine return
    """

    return asyncio.get_event_loop().run_until_complete(coroutine)
