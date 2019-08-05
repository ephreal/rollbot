# -*- coding: utf-8 -*-

"""
Copyright 2019 Ephreal

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


class TestBlackjackHandler(unittest.TestCase):

    def setUp(self):
        self.handler = game_handler.BlackjackHandler()

        self.player = player.BlackjackPlayer(
            name="Freido",
            id=314,
            hand=[]
        )
        self.handler.add_player(self.player)
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

        self.handler.setup()
        start = self.dealer.tally
        self.handler.dealer_play()

        if start >= 17:
            self.assertEqual(start, self.dealer.tally)
        else:
            self.assertNotEqual(start, self.dealer.tally)

    def test_double_hit(self):
        """
        tests taking two cards from the deck at once.
        """
        self.handler.double_hit(self.player)

        self.assertTrue(self.player.tally > 0)
        self.assertEqual(len(self.player.hand), 2)
        self.assertEqual(len(self.handler.deck), 50)

    def test_hit(self):
        """
        Tests taking a card from the deck
        """
        self.handler.hit(self.player)

        self.assertTrue(self.player.tally > 0)
        self.assertEqual(len(self.player.hand), 1)
        self.assertEqual(len(self.handler.deck), 51)

    def test_setup(self):
        """
        Makes sure that the setup function deals the correct amount of cards
        to all players.
        """

        self.handler.setup()

        self.assertEqual(len(self.player.hand), 2)
        self.assertEqual(len(self.dealer.hand), 2)

    def test_stand(self):
        """
        Makes sure that stand sets the correct player to play
        """

        self.handler.stand()
        self.assertEqual(self.handler.current_player, 0)


if __name__ == "__main__":
    unittest.main()
