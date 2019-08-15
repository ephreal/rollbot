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
from mock import MockUsers


class TestDiscordInterface(unittest.TestCase):

    def setUp(self):

        self.interface = discord_interface.DiscordInterface()
        self.test_user = MockUsers.DiscordUser(userid=10, name="Glaxion")

    def test_add_game_handler(self):
        """
        Verifies that the add_game_handler function does what it says
        """

        self.interface.add_game_handler("blackjack")
        self.assertEqual(len(self.interface.current_sessions), 1)

        self.interface.add_game_handler("BLACKJACK")
        self.assertEqual(len(self.interface.current_sessions), 2)

    def test_generate_id(self):
        """
        Makes sure that generate_id returns a valid int
        """

        session_id = self.interface.generate_session()

        self.assertTrue(isinstance(session_id, int))

        session_id = str(session_id)
        self.assertEqual(len(session_id), 11)

    def test_get_game_state_by_member(self):
        """
        Verifies that the game state is created and returned
        """

        player = self.interface.make_player(self.test_user)
        session = self.interface.add_game_handler("blackjack")
        self.interface.add_player_to_current_players(player, session)
        self.interface.add_player_to_game(player)
        state = self.interface.get_game_state_by_member(self.test_user)

        self.assertEqual(state.current_player.name, "Glaxion")
        self.assertEqual(state.handler,
                         self.interface.current_sessions[session])

    def test_make_player(self):
        """
        Tests the make player portion of the discord interface.
        """

        player = self.interface.make_player(self.test_user)
        self.assertEqual(player.id, 10)
        self.assertEqual(player.name, "Glaxion")

    def test_add_player_to_game(self):
        """
        tests to make sure a player is added to the game properly
        """
        pass
