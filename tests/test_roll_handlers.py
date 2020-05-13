# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

import asyncio
import unittest
from utils.rolling import handlers


class TestBaseRollHandler(unittest.TestCase):
    def setUp(self):
        self.handler = handlers.BaseRollHandler()

    def test_roll(self):
        """
        Ensures that the handler successfully rolls and returns a BaseRoll
        object that contains rolls
        """
        roll = run(self.handler.roll(["3d6"]))
        self.assertEqual(len(roll.result), 3)
        self.assertEqual(roll.note, None)


def run(coroutine):
    """
    Runs and returns the data from the couroutine passed in. This is to
    only be used in unittesting.

    coroutine : asyncio coroutine

        -> coroutine return
    """

    return asyncio.get_event_loop().run_until_complete(coroutine)
