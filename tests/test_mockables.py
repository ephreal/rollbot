# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

import unittest
from tests.mock import mockables


class TestMockables(unittest.TestCase):
    def setUp(self):
        pass

    def test_bot1(self):
        """Verifies bot1 is setup properly"""
        self.assertEqual(mockables.bot1.restrict_rolling, True)

    def test_bot2(self):
        """Verifies bot1 is setup properly"""
        self.assertEqual(mockables.bot2.restrict_rolling, False)

    def test_context1(self):
        """Verifies context1 is set up and accessible correctly"""
        self.assertEqual(mockables.context1.guild.name, "guild1")
        self.assertEqual(mockables.context1.channel.name, "general")

    def test_context2(self):
        """Verifies context2 is set up and accessible correctly"""
        self.assertEqual(mockables.context2.guild.name, "guild2")
        self.assertEqual(mockables.context2.channel.name, "rolling")

    def test_context3(self):
        """Verifies context3 is set up and accessible correctly"""
        self.assertEqual(mockables.context3.guild.name, "guild3")
        self.assertEqual(mockables.context3.channel.name, "conspiracy")

    def test_guild1(self):
        """verifies guild1 is set up correctly"""
        self.assertEqual(len(mockables.guild1.text_channels), 4)
        self.assertEqual(len(mockables.guild1.users), 7)

    def test_guild2(self):
        """Verifies guild2 is setup properly"""
        self.assertEqual(len(mockables.guild2.text_channels), 5)
        self.assertEqual(len(mockables.guild2.users), 4)

    def test_guild3(self):
        """Verifies guild 3 is setup properly"""
        self.assertEqual(len(mockables.guild3.text_channels), 3)
        self.assertEqual(len(mockables.guild3.users), 5)
