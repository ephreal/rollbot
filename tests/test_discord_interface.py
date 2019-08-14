# -*- coding: utf-8 -*-

"""
Copyright 2018-2019 Ephreal

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import unittest
from classes.games import discord_interface


class TestDiscordInterface(unittest.TestCase):

    def setUp(self):

        self.interface = discord_interface.DiscordInterface()

    def test_add_game_handler(self):

        self.interface.add_game_handler("blackjack")
        self.assertEqual(len(self.interface.current_sessions), 1)

        self.interface.add_game_handler("BLACKJACK")
        self.assertEqual(len(self.interface.current_sessions), 2)

    def test_generate_id(self):

        session_id = self.interface.generate_session()

        self.assertTrue(isinstance(session_id, int))

        session_id = str(session_id)
        self.assertEqual(len(session_id), 11)
