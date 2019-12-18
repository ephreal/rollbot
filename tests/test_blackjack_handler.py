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


# methods still needing test coverage:
#       check_tally
#       check_commands
#       expose_commands

class TestBlackjackHandler(unittest.TestCase):

    def setUp(self):
        self.handler = game_handler.BlackjackHandler()

        self.player = player.BlackjackPlayer(
            name="Freido",
            player_id=314,
            hand=[]
        )
        run(self.handler.add_player(self.player))
        self.dealer = self.handler.players[0]

    def test_initialization(self):
        """
        Verifies that initialization sets things to a sane state
        """

        self.assertEqual(self.handler.current_player, 1)
        self.assertFalse(self.handler.current_ties)
        self.assertFalse(self.handler.current_winner)
        self.assertEqual(self.handler.highest_score, 0)
        self.assertEqual(self.handler.players[0], self.handler.dealer)

    def test_dealer_play(self):
        """
        Tests to make sure the dealer plays the game. Does not assure that
        the dealer can play well, however.
        """

        run(self.handler.setup())
        start = self.dealer.tally
        run(self.handler.dealer_play())

        if start >= 17:
            self.assertEqual(start, self.dealer.tally)
        else:
            self.assertNotEqual(start, self.dealer.tally)

    def test_double_hit(self):
        """
        tests taking two cards from the deck at once.
        """
        run(self.handler.double_hit(self.player))

        self.assertTrue(self.player.tally > 0)
        self.assertEqual(len(self.player.hand), 2)
        self.assertEqual(len(self.handler.deck), 50)

    def test_hit(self):
        """
        Tests taking a card from the deck
        """
        run(self.handler.hit(self.player))

        self.assertTrue(self.player.tally > 0)
        self.assertEqual(len(self.player.hand), 1)
        self.assertEqual(len(self.handler.deck), 51)

    def test_setup(self):
        """
        Makes sure that the setup function deals the correct amount of cards
        to all players.
        """

        run(self.handler.setup())

        self.assertEqual(len(self.player.hand), 2)
        self.assertEqual(len(self.dealer.hand), 2)

    def test_stand(self):
        """
        Makes sure that stand sets the correct player to play
        """

        run(self.handler.stand())
        self.assertEqual(self.handler.current_player, 0)


if __name__ == "__main__":
    unittest.main()
