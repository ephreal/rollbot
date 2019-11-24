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
from classes.games import deck
from classes.games import card


class TestDeckMethods(unittest.TestCase):

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

        self.deck = deck.Deck(self.cards)

    def test_len(self):
        """
        Makes sure that the __len__ function returns the correct amount
        """

        self.assertEqual(len(self.deck), 13)
        self.deck.draw(5)
        self.assertEqual(len(self.deck), 8)

    def test_add_discarded(self):
        """
        Verifies that all discarded cards are added back to the deck.
        """
        self.deck.discard_from_top(5)
        self.deck.add_discarded()
        self.assertTrue(not self.deck.discarded)
        self.assertTrue(len(self.deck.cards) == len(self.cards))

    def test_check_cards(self):
        """
        Checks to make sure that check_cards adds cards back to the deck
        from the discard pile when more cards need to be taken from the
        deck than exist.
        """

        self.deck.discard_from_top(10)
        self.deck.check_cards(8)

        self.assertTrue(not self.deck.discarded)
        self.assertTrue(len(self.deck.cards) == len(self.cards))

    def test_clean_deck(self):
        """
        Verifies that clean_deck remains unchanged after the deck is
        initialized
        """
        self.assertEqual(self.deck.clean_deck, self.cards)

    def test_cut_deck(self):
        """
        Checks that cutting the deck works as intended.
        """
        cut_cards = self.deck.cards[6:].extend(self.deck.cards[:6])
        self.deck.cut(6)
        self.assertEqual(self.deck.cards, cut_cards)

    def test_discard_from_bottom(self):
        """
        Checks that discarding cards from the bottom of the deck works as
        expected
        """

        discarded = self.deck.cards[-4:]
        self.deck.discard_from_bottom(4)
        self.assertEqual(discarded, self.deck.discarded)
        total_len = len(self.deck.cards) + len(discarded)
        self.assertEqual(total_len, len(self.deck.clean_deck))

    def test_discard_from_hand(self):
        """
        Verifies that discarding a card from the hand places the card in the
        discard pile.
        """
        drawn = self.deck.random_card()
        self.deck.discard_from_hand(drawn)

        self.assertEqual([drawn], self.deck.discarded)
        self.assertTrue(len(self.deck.in_hand) == 0)

    def test_discard_from_middle(self):
        """
        Verifies that discarding from the middle of the deck works
        """

        start_point = int(len(self.deck.cards) / 2)
        cards = self.deck.cards[start_point: start_point + 4]
        self.deck.discard_from_middle(4)

        self.assertEqual(cards, self.deck.discarded)

    def test_discard_from_deck_randomly(self):
        """
        Verifies that random discarding works as expected.
        """

        self.deck.discard_from_deck_randomly(5)
        self.assertTrue(len(self.deck.discarded) == 5)
        self.assertEqual(len(self.deck.cards) + 5, len(self.deck.clean_deck))

    def test_discard_from_top(self):
        """
        Verifies that discarding cards from the top of the deck is functioning
        properly.
        """

        self.deck.discard_from_top(3)
        self.assertTrue(len(self.deck.discarded) == 3)
        self.assertTrue(len(self.deck.cards) == len(self.deck.clean_deck) - 3)

    def test_drawing(self):
        """
        Test the ability to draw cards. Verifies that cards are properly
        placed into the in_hand variable.
        """
        drawn = self.deck.draw(5)

        self.assertEqual(len(drawn), 5)
        self.assertEqual(self.deck.in_hand, drawn)

    def test_place_card(self):
        """
        Tests the ability to place cards by string into the deck.
        """

        drawn = self.deck.random_card()
        self.deck.place_card(drawn, 5)
        # Remember now... lists start at 0!
        self.assertEqual(drawn, self.deck.cards[4])
        self.assertEqual(len(self.deck.cards), len(self.deck.clean_deck))
        self.assertEqual(self.deck.in_hand, [])
        self.assertEqual(self.deck.discarded, [])

    def test_place_cards(self):
        """
        Tests the ability to place cards by list into the deck
        """

        drawn = self.deck.draw(5)
        self.deck.place_cards(drawn, 5)

        self.assertEqual(drawn, self.deck.cards[4:9])
        self.assertEqual(len(self.deck.cards), len(self.deck.clean_deck))
        self.assertEqual(self.deck.in_hand, [])
        self.assertEqual(self.deck.discarded, [])

    def test_random_card(self):
        """
        Verifies that getting a random card adds to variables correctly
        """

        card = self.deck.random_card()

        self.assertTrue(self.deck.in_hand[0] == card)
        self.assertTrue(card not in self.deck.cards)

        card = self.deck.random_card()

        self.assertTrue(self.deck.in_hand[1] == card)
        self.assertTrue(card not in self.deck.cards)

    def test_reset(self):
        """
        Verifies that deck.reset() is able to bring the deck to a clean state
        """

        self.deck.draw(5)
        test = self.deck.random_card()
        self.deck.up_last(test)
        self.deck.reset()

        self.assertTrue(self.deck.clean_deck)
        self.assertFalse(self.deck.discarded)
        self.assertFalse(self.deck.in_hand)
        self.assertNotEqual(self.deck.clean_deck, self.deck.cards)

    def test_shuffle(self):
        """
        Verifies that shuffling the cards only changes self.cards
        """

        cards = self.deck.cards[:]

        self.deck.shuffle()
        self.assertFalse(cards == self.deck.cards)

    def test_up_first(self):
        """
        Makes sure that inserting both a string and a list work as intended
        """
        drawn = self.deck.random_card()
        self.deck.up_next(drawn)
        self.assertEqual(drawn.worth, self.deck.cards[0].worth)
        self.assertEqual(len(self.deck.cards), len(self.deck.clean_deck))

    def test_up_last(self):
        """
        Makes sure that inserting both a string and a list work as intended
        """
        drawn = self.deck.random_card()
        self.deck.up_last(drawn)
        self.assertEqual(drawn.worth, self.deck.cards[-1].worth)
        self.assertEqual(len(self.deck.cards), len(self.deck.clean_deck))

    def test_draw_all_cards(self):
        """
        Tests to make sure that Deck.draw() works sanely when cards run out.
        """
        cards = self.deck.draw(13)
        self.assertTrue(self.deck.cards == [])
        self.assertTrue(len(cards) == len(self.cards))

        new_card = self.deck.draw(1)
        self.assertTrue(self.deck.cards == [])
        self.assertTrue(new_card == [])

        self.deck.discard_from_hand(cards)
        self.deck.draw(5)
        self.assertTrue(len(self.deck.cards) == len(self.cards) - 5)
        self.assertTrue(self.deck.discarded == [])

    def test_random_draw_all_cards(self):
        """
        Tests to make sure that Deck.random_card() works properly when no
        cards remain to be drawn.
        """

        self.deck.discard_from_top(len(self.cards)-1)
        cards = []
        cards.append(self.deck.random_card())
        self.assertFalse(self.deck.cards)

        cards.append(self.deck.random_card())
        self.assertTrue(cards == self.deck.in_hand)
        self.assertTrue(len(self.deck.cards) == len(self.cards)-2)

    def test_standard_deck(self):
        """
        Makes sure that a standard deck is able to be created from the base
        deck class.
        """
        self.deck_type = "standard"
        standard_deck = deck.StandardDeck()

        y = standard_deck.random_card()
        self.assertTrue(y not in standard_deck.cards)
        self.assertTrue(y in standard_deck.in_hand)

        standard_deck.discard_from_hand(y)
        self.assertTrue(y in standard_deck.discarded)
        self.assertTrue(y not in standard_deck.in_hand)

    def test_uno_deck(self):
        """
        Verifies that the uno deck can be created from the base deck class
        without any issues.
        """

        uno_deck = deck.UnoDeck()

        y = uno_deck.random_card()
        # There should always be an odd number of cards of that type remaining
        self.assertTrue(uno_deck.cards.count(y) % 2 == 1)
        self.assertTrue(y in uno_deck.in_hand)

        uno_deck.discard_from_hand(y)
        self.assertTrue(y in uno_deck.discarded)
        self.assertTrue(y not in uno_deck.in_hand)


if __name__ == "__main__":
    unittest.main()
