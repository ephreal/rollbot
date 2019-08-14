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
from classes.games import game_handler
from classes.games import player
from classes.games import deck


class TestGameHandler(unittest.TestCase):

    def setUp(self):
        self.standard_handler = game_handler.CardGameHandler(
            deck=deck.StandardDeck(),
            players=[]
        )

        self.player = player.CardPlayer(name="gorlog", hand=[],
                                        player_id=1234567890)

    def test_add_players(self):
        """
        Verifies that adding players works properly
        """
        self.standard_handler.add_player(self.player)

        self.assertTrue(len(self.standard_handler.players) == 1)
        self.assertTrue(self.standard_handler.players[0].name == "gorlog")

        [
           self.standard_handler.add_player(self.player)
           for _ in range(0, 10)
        ]

        self.assertTrue(len(self.standard_handler.players) == 11)

    def test_construct_and_add_players(self):
        """
        Verifies that the game_handler is able to build and add players to the
        game.
        """

        self.standard_handler.construct_and_add_player(name="gorlog",
                                                       player_id=1234567890,
                                                       hand=[])

        self.assertTrue(len(self.standard_handler.players) == 1)

    def test_deal(self):
        """
        Verifies that cards are dealt to players correctly
        """

        self.standard_handler.add_player(self.player)
        cards = self.standard_handler.deal(5, self.player)
        self.assertEqual(self.standard_handler.players[0].hand, cards)
        self.assertEqual(self.player.hand, cards)

    def test_get_next_player(self):
        """
        Verifies that get_next_player returns the correct player
        """

        new_player = player.CardPlayer(name="gorlog", player_id=1234567890,
                                       hand=[])
        [
            self.standard_handler.add_player(new_player) for _ in range(0, 10)
        ]

        self.assertEqual(self.standard_handler.current_player, 0)
        next_player = self.standard_handler.get_next_player()
        self.assertEqual(next_player[0], 1)

        self.standard_handler.current_player += 1
        next_player = self.standard_handler.get_next_player()
        self.assertEqual(next_player[0], 2)

    def test_remove_player_by_id(self):
        """
        Tests removing a player by their player_id
        """
        self.standard_handler.add_player(self.player)
        self.standard_handler.remove_player_by_id(1234567890)
        self.assertFalse(self.standard_handler.players)
        self.assertTrue(self.standard_handler.players == [])

    def test_remove_by_index(self):
        """
        Tests removing a player by index
        """
        self.standard_handler.add_player(self.player)
        self.standard_handler.remove_player_by_index(0)
        self.assertFalse(self.standard_handler.players)
        self.assertTrue(self.standard_handler.players == [])

    def test_remove_player_by_name(self):
        """
        Tests removing a player by their id
        """
        self.standard_handler.add_player(self.player)
        self.standard_handler.remove_player_by_name("gorlog")
        self.assertFalse(self.standard_handler.players)
        self.assertTrue(self.standard_handler.players == [])

    def test_set_current_player_by_id(self):
        """
        Tests that the current player can be set by id
        """
        challenger = player.CardPlayer(name="zippy", player_id=20, hand=[])
        self.standard_handler.add_player(self.player)
        self.standard_handler.add_player(challenger)

        self.standard_handler.set_current_player_by_id(20)
        self.assertEqual(self.standard_handler.current_player, 1)

        self.standard_handler.set_current_player_by_id(1234567890)
        self.assertEqual(self.standard_handler.current_player, 0)

    def test_set_current_player_by_index(self):
        """
        Tests setting the current player by index.
        """

        challenger = player.CardPlayer(name="zippy", player_id=20, hand=[])
        self.standard_handler.add_player(self.player)
        self.standard_handler.add_player(challenger)

        self.standard_handler.set_current_player_by_index(1)
        self.assertEqual(self.standard_handler.current_player, 1)

        self.standard_handler.set_current_player_by_index(50)
        self.assertEqual(self.standard_handler.current_player, 0)

    def test_set_current_player_by_name(self):
        """
        Tests the setting of current players by name
        """

        challenger = player.CardPlayer(name="zippy", player_id=20, hand=[])
        self.standard_handler.add_player(self.player)
        self.standard_handler.add_player(challenger)

        self.standard_handler.set_current_player_by_name("zippy")
        self.assertEqual(self.standard_handler.current_player, 1)

        self.standard_handler.set_current_player_by_name("gorlog")
        self.assertEqual(self.standard_handler.current_player, 0)


if __name__ == "__main__":
    unittest.main()
