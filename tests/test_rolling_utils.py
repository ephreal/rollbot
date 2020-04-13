# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

import asyncio
import unittest
from tests.mock import mockables
from utils import rolling_utils


class TestRollingUtils(unittest.TestCase):
    def setUp(self):
        pass

    def test_check_roll_channel(self):
        """Verifies roll channel is properly found"""
        # This SHOULD find the rolling channel
        ctx = mockables.context1
        bot1 = mockables.bot1
        bot2 = mockables.bot2

        channel = run(rolling_utils.check_roll_channel(ctx, bot1))
        self.assertNotEqual(mockables.context1.channel.name, channel.name)

        channel = run(rolling_utils.check_roll_channel(ctx, bot2))
        self.assertEqual(mockables.context1.channel.name, channel.name)

        ctx = mockables.context2

        # These should return the same channel
        channel = run(rolling_utils.check_roll_channel(ctx, bot1))
        self.assertEqual(mockables.context2.channel.name, channel.name)

        channel = run(rolling_utils.check_roll_channel(ctx, bot2))
        self.assertNotEqual(mockables.context1.channel.name, channel.name)

        ctx = mockables.context3

        channel = run(rolling_utils.check_roll_channel(ctx, bot1))
        self.assertEqual(mockables.context3.channel.name, channel.name)

        channel = run(rolling_utils.check_roll_channel(ctx, bot2))
        self.assertNotEqual(mockables.context1.channel.name, channel.name)


def run(coroutine):
    """
    Runs and returns the data from the couroutine passed in. This is to
    only be used in unittesting.

    coroutine : asyncio coroutine

        -> coroutine return
    """

    return asyncio.get_event_loop().run_until_complete(coroutine)
