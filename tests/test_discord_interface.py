# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

import unittest
from classes.games import discord_interface
from mock import MockUsers
from tests.asyncio_run import run

print("Tests still need to be completed for "
      "discord_interface.add_player_to_game")


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

    def test_add_player_to_game(self):
        """
        tests to make sure a player is added to the game properly
        """
        pass

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
        run(self.interface.add_player_to_current_players(player, session))
        run(self.interface.add_player_to_game(player))
        state = run(self.interface.get_game_state_by_member(self.test_user))

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
