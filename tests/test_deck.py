import unittest
from classes import deck


class TestDeckMethods(unittest.TestCase):

    def setUp(self):
        cards = ["ace", "two", "three", "four", "five", "six", "seven",
                 "eight", "nine", "jack", "queen", "king"]

        self.deck = deck.Deck(cards)

    def test_clean_deck(self):
        """
        Verifies that clean_deck remains unchanged after the deck is
        initialized
        """
        cards = ["ace", "two", "three", "four", "five", "six", "seven",
                 "eight", "nine", "jack", "queen", "king"]
        self.assertEqual(self.deck.clean_deck, cards)

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
        self.assertEqual(drawn, self.deck.cards[0])
        self.assertEqual(len(self.deck.cards), len(self.deck.clean_deck))

    def test_up_last(self):
        """
        Makes sure that inserting both a string and a list work as intended
        """
        drawn = self.deck.random_card()
        self.deck.up_last(drawn)
        self.assertEqual(drawn, self.deck.cards[-1])
        self.assertEqual(len(self.deck.cards), len(self.deck.clean_deck))


if __name__ == "__main__":
    unittest.main()
