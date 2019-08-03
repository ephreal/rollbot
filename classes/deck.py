# -*- coding: utf-8 -*-

"""
Copyright 2018 Ephreal

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

import random


class Deck():
    """
    A base class that has the required methods for building, drawing from,
    and adding cards back into a deck.

    Class Variables

        cards (str list):
                A list of all cards in the deck.

        clean_deck (str list):
                An ordered list of all cards in the deck.

        discarded (str list):
                A list of all cards in the discard pile

    Class Functions

        Deck.add_discarded():
            Places all discarded card back into self.cards

        Deck.cut(position: int):
            Cuts the deck at the index specified by position - 1.

        Deck.draw(amount: int):
            Draws a specified amount of cards from the deck

        Deck.place_card(card: str, position: int):
            Places a card at the specified position in the deck. If the
            position specified is greater than the remaining cards, it places
            the cards at the end.

        Deck.place_cards(cards: lins[str], position: int):
            Places cards in at a given point. If the position specified
            specified is greater than the remaining cards, it places the cards
            at the end.

        Deck.random_card():
            Draws a card from the deck randomly.

        Deck.reset():
            Sets self.cards to self.clean_deck

        Deck.shuffle():
            Shuffles the cards list

        Deck.up_next(card: str):
            Special alias for Deck.place_card() and Deck.place_cards(). Places
            the card(s) in the deck at position 0.

        Deck.up_last(card: str):
            Special alias for Deck.place_card() and Deck.place_cards(). Places
            the card(s) back into the deck at the very end.
    """
    def __init__(self, cards):
        self.clean_deck = cards[:]

        # prepare deck for first use
        random.shuffle(cards)
        self.cards = cards
        self.discarded = []

    def add_discarded(self) -> None:
        """
        Adds cards from the discarded pile back into the main card deck.

        Returns None
        """

        random.shuffle(self.discarded)
        self.cards.append(self.discarded)
        self.discarded = []

    def cut(self, position) -> None:
        """
        Cuts the deck at position - 1. The second half of the deck is placed
        on top on the deck. If the position is too high or too low, the deck
        will be cut in half.
        """

        if not position:
            position = len(self.cards / 2)

        if position <= 0 or position >= len(self.cards)-1:
            position = len(self.cards / 2)

        back = self.cards[position:]
        self.cards = self.cards[:position]
        self.cards = back.extend(self.cards)

    def draw(self, amount=1):
        """
        Draws a specified amount of cards from the deck. If the deck would run
        out of cards and cards exist in self.discarded, it will call
        self.add_discarded, self.shuffle, and continue trying to deal cards. If
        no cards can be drawn, it will return an empty list.

        draw(amount: int)
            Returns a str list.
        """

        if not self.cards and self.discarded:
            self.add_discarded()

        elif not self.cards:
            return []

        # Check if we need more cards than are available
        if len(self.cards) < amount and not self.discarded:
            drawn_cards = self.cards

        elif len(self.cards) < amount and self.discarded:
            self.add_discarded()

        drawn_cards = self.cards[0:amount]
        self.discarded.append(drawn_cards)
        self.cards = self.cards[amount:]

        return drawn_cards

    def place_card(self, card, position):
        """
        Places a card at a given point in the deck. If you need to place
        multiple cards in at a point, use place_cards instead.

        ie: place_card("king", 3) inserts the king at index 2 in the deck.

        If the card can not be placed at the index (maybe that index doesn't
        exist), the card will be placed at the very end.

        returns None
        """
        try:
            self.cards.insert(position-1, card)

        except IndexError:
            # That position does not exist, place the card at the end
            self.cards.append(card)

    def place_cards(self, cards, position):
        """
        Places multiple cards in the deck, starting with the first card
        in cards inserted at position, the second card in cards inserted at
        position + 1, and so an.

        Calls place_cards() for all insertion.
        """

        for i in range(0, len(cards)):
            self.place_card(cards[i], position + i)

    def random_card(self):
        """
        Returns a random card from the deck. If the deck is empty, it returns
        an empty string.
        """

        if len(self.cards) == 0:
            return ""

        card = random.choice(self.cards)
        self.cards.remove(card)
        return card

    def reset(self):
        """
        Resets the deck to a clean state and prepares cards for use by
        shuffling the cards.
        """

        self.cards = self.clean_deck[:]
        self.discarded = []
        self.shuffle()

    def shuffle(self):
        """
        Shuffles all cards in self.cards.
        """

        random.shuffle(self.cards)

    def up_next(self, card):
        """
        Places the card(s) at the front of the deck. If a list is passed in,
        it places the cards into the deck in the order specified.
        """

        if isinstance(card, str):
            self.place_card(card, 1)

        elif isinstance(card, list):
            if len(card) == 1:
                self.place_card(card[0], 1)
            else:
                self.place_cards(card, 1)

    def up_last(self, card):
        """
        Places the card(s) at the end of the deck.If a list is passed in, it
        places the cards into the deck in the same order.
        """

        if isinstance(card, str):
            self.place_card(card, len(self.cards)+1)

        elif isinstance(card, list):
            if len(card) == 1:
                self.place_card(card, len(self.cards+1))
            else:
                self.place_cards(card, len(self.cards)+1)
