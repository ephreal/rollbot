# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""


from mock import MockUsers
import unittest
from classes.games import player
from classes.games import card


class TestPlayersMethods(unittest.TestCase):

    def setUp(self):
        self.cards = [
            card.Card(name="ace", worth=1),
            card.Card(name="two", worth=2),
            card.Card(name="three", worth=3),
            card.Card(name="four", worth=4),
            card.Card(name="five", worth=5),
            card.Card(name="six", worth=6),
            card.Card(name="seven", worth=7),
            card.Card(name="eight", worth=8),
            card.Card(name="nine", worth=9),
            card.Card(name="ten", worth=10),
            card.Card(name="jack", worth=10),
            card.Card(name="queen", worth=10),
            card.Card(name="king", worth=10)
        ]

        user = MockUsers.DiscordUser(userid=1234567890, name="test_player")
        self.player = player.Player(user, "test_player", 1234567890)
        self.card_player = player.CardPlayer(name="card_player",
                                             player_id=9876543210,
                                             hand=[])

        self.blackjack_player = player.BlackjackPlayer(name="liggan",
                                                       player_id=1336,
                                                       hand=[])

    def test_player_variables(self):
        """
        Makes sure the player variables are able to be set properly
        """

        self.assertTrue(self.player.name == "test_player")
        self.assertTrue(self.player.id == 1234567890)

        self.assertTrue(self.card_player.name == "card_player")
        self.assertTrue(self.card_player.id == 9876543210)
        self.assertTrue(self.card_player.hand == [])

    def test_card_player_add_card(self):
        """
        Verifies that CardPlayer.add_card_to_hand() adds a card to it's hand
        """

        self.card_player.add_card_to_hand("ace")
        self.assertTrue("ace" in self.card_player.hand)

    def test_card_player_add_cards(self):
        """
        Verifies that CardPlayer.add_cards_to_hand() adds cards to hand as
        expected.
        """

        self.card_player.add_cards_to_hand(self.cards)
        self.assertTrue(self.cards == self.card_player.hand)

    def test_card_player_remove_card(self):
        """
        Verifies that removing a card from the player's works expected
        """

        self.card_player.add_cards_to_hand(self.cards)
        self.card_player.remove_card_from_hand(self.cards[4])
        self.assertTrue(self.card_player.hand[4].worth == 6)

    def test_card_player_remove_cards(self):
        """
        Verifies that removing cards from a player's hand works as expected
        """

        self.card_player.add_cards_to_hand(self.cards)
        self.card_player.remove_cards_from_hand(self.cards[:12])
        self.assertTrue(self.card_player.hand[0] == self.cards[12])
        self.assertEqual(len(self.card_player.hand), 1)
        self.assertTrue(self.cards[12:] == self.card_player.hand)

    def test_blackjack_player(self):
        """
        Makes sure that the blackjack player initializes everything prpoerly.
        """

        self.assertFalse(self.blackjack_player.bust)
        self.assertEqual(self.blackjack_player.tally, 0)

    def test_blackjack_player_receive_card(self):
        """
        Verifies that the receive_card function increments the tally correctly
        """

        self.blackjack_player.receive_card(self.cards[11])
        self.assertEqual(self.blackjack_player.tally, 10)
        # Make sure that the bust boolean will get set
        self.blackjack_player.receive_card(self.cards[11])
        self.blackjack_player.receive_card(self.cards[11])
        self.assertTrue(self.blackjack_player.bust)

    def test_blackjack_player_receive_cards(self):
        """
        Makes sure that the receive_cards function works as expected
        """

        self.blackjack_player.receive_cards(self.cards[3:5])
        self.assertEqual(self.blackjack_player.tally, 9)


if __name__ == "__main__":
    unittest.main()
