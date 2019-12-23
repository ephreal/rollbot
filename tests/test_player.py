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
            card.Card(name="ace", value=1),
            card.Card(name="two", value=2),
            card.Card(name="three", value=3),
            card.Card(name="four", value=4),
            card.Card(name="five", value=5),
            card.Card(name="six", value=6),
            card.Card(name="seven", value=7),
            card.Card(name="eight", value=8),
            card.Card(name="nine", value=9),
            card.Card(name="ten", value=10),
            card.Card(name="jack", value=10),
            card.Card(name="queen", value=10),
            card.Card(name="king", value=10)
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
        self.assertEqual(self.card_player.hand[4].value, 6)

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

        self.blackjack_player.add_cards_to_hand(self.cards[11:12])
        self.assertEqual(self.blackjack_player.tally, 10)
        # Make sure that the bust boolean will get set
        self.blackjack_player.add_cards_to_hand(self.cards[11:12])
        self.blackjack_player.add_cards_to_hand(self.cards[11:12])
        self.assertTrue(self.blackjack_player.bust)

    def test_blackjack_player_receive_cards(self):
        """
        Makes sure that the receive_cards function works as expected
        """

        self.blackjack_player.add_cards_to_hand(self.cards[3:5])
        self.assertEqual(self.blackjack_player.tally, 9)


if __name__ == "__main__":
    unittest.main()
