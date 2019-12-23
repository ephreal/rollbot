# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""


from tests.asyncio_run import run
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
        run(self.standard_handler.add_player(self.player))

        self.assertTrue(len(self.standard_handler.players) == 1)
        self.assertTrue(self.standard_handler.players[0].name == "gorlog")

        for _ in range(0, 10):
            run(self.standard_handler.add_player(self.player))

        self.assertTrue(len(self.standard_handler.players) == 11)

    def test_construct_and_add_players(self):
        """
        Verifies that the game_handler is able to build and add players to the
        game.
        """

        run(self.standard_handler.construct_and_add_player(
            name="gorlog",
            player_id=1234567890,
            hand=[]))

        self.assertTrue(len(self.standard_handler.players) == 1)

    def test_deal(self):
        """
        Verifies that cards are dealt to players correctly
        """

        run(self.standard_handler.add_player(self.player))
        cards = run(self.standard_handler.deal(5, self.player))
        self.assertEqual(self.standard_handler.players[0].hand, cards)
        self.assertEqual(self.player.hand, cards)

    def test_get_current_player(self):
        """
        Verifies that the correct player is returned
        """
        second_player = player.CardPlayer(name="draxx", hand=[],
                                          player_id=1234567890)

        run(self.standard_handler.add_player(self.player))
        run(self.standard_handler.add_player(second_player))
        self.assertEqual(run(self.standard_handler.get_current_player()),
                         self.standard_handler.players[0])

        run(self.standard_handler.advance_to_next_player())
        self.assertEqual(run(self.standard_handler.get_current_player()),
                         self.standard_handler.players[1])

    def test_get_next_player(self):
        """
        Verifies that get_next_player returns the correct player
        """

        new_player = player.CardPlayer(name="gorlog", player_id=1234567890,
                                       hand=[])
        for _ in range(0, 10):
            run(self.standard_handler.add_player(new_player))

        self.assertEqual(self.standard_handler.current_player, 0)
        next_player = run(self.standard_handler.get_next_player())
        self.assertEqual(next_player[0], 1)

        self.standard_handler.current_player += 1
        next_player = run(self.standard_handler.get_next_player())
        self.assertEqual(next_player[0], 2)

    def test_remove_player_by_id(self):
        """
        Tests removing a player by their player_id
        """
        run(self.standard_handler.add_player(self.player))
        run(self.standard_handler.remove_player_by_id(1234567890))
        self.assertFalse(self.standard_handler.players)
        self.assertTrue(self.standard_handler.players == [])

    def test_remove_player_by_name(self):
        """
        Tests removing a player by their id
        """
        run(self.standard_handler.add_player(self.player))
        run(self.standard_handler.remove_player_by_name("gorlog"))
        self.assertFalse(self.standard_handler.players)
        self.assertTrue(self.standard_handler.players == [])

    def test_set_current_player_by_id(self):
        """
        Tests that the current player can be set by id
        """
        challenger = player.CardPlayer(name="zippy", player_id=20, hand=[])
        run(self.standard_handler.add_player(self.player))
        run(self.standard_handler.add_player(challenger))

        run(self.standard_handler.set_current_player_by_id(20))
        self.assertEqual(self.standard_handler.current_player, 1)

        run(self.standard_handler.set_current_player_by_id(1234567890))
        self.assertEqual(self.standard_handler.current_player, 0)

    def test_set_current_player_by_name(self):
        """
        Tests the setting of current players by name
        """

        challenger = player.CardPlayer(name="zippy", player_id=20, hand=[])
        run(self.standard_handler.add_player(self.player))
        run(self.standard_handler.add_player(challenger))

        run(self.standard_handler.set_current_player_by_name("zippy"))
        self.assertEqual(self.standard_handler.current_player, 1)

        run(self.standard_handler.set_current_player_by_name("gorlog"))
        self.assertEqual(self.standard_handler.current_player, 0)


if __name__ == "__main__":
    unittest.main()
