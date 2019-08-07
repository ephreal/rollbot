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

import random
from .card import Card


class Deck():
    """
    A base class that has the required methods for building, drawing from,
    and adding cards back into a deck.

    Class Variables

        cards (list[card.Card]):
                A list of all cards in the deck.

        clean_deck (str list):
                An ordered list of all cards in the deck.

        discarded (str list):
                A list of all cards in the discard pile

        in_hands (str list)
                A list of all cards currently in player's hands

    Class Functions

        Deck.add_discarded():
            Places all discarded card back into self.cards

        Deck.check_cards(amount: int)
            Check the amount of cards remaining in the deck against the
            amount of cards to be drawn from the deck. If more cards need to
            be drawn than are in the deck, and discarded cards exist,
            it places the discarded cards back into the deck with
            Deck.add_discarded().

        Deck.cut(position: int):
            Cuts the deck at the index specified by position - 1.

        Deck.discard_from_bottom(amount: int):
            Places cards in the discard pile directly from the bottom of the
            deck.

        Deck.discard_from_deck_randomly(amount: int):
            Places cards in the discard pile randomly from the deck.

        Deck.discard_from_top(amount: int):
            Places cards in the discard pile directly from the middle of the
            deck.

        Deck.discard_from_top(amount: int):
            Places cards in the discard pile directly from the top of the deck.

        Deck.discard_from_hand(card: str or list):
            places cards in self.discarded when cards are given back.

        Deck.draw(amount: int):
            Draws a specified amount of cards from the deck

        Deck.place_card(card: str, position: int):
            Places a card at the specified position in the deck. If the
            position specified is greater than the remaining cards, it places
            the cards at the end.

        Deck.place_cards(cards: list[str], position: int):
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
        # And today I learned a lesson about why taking a copy of a list is
        # a GoodThing.
        self.clean_deck = cards[:]

        # prepare deck for first use
        self.cards = cards[:]
        self.shuffle()
        self.discarded = []
        self.in_hand = []

    def __len__(self):
        """
        Returns the amount of cards in the deck
        """
        return len(self.cards)

    def add_discarded(self):
        """
        Adds cards from the discarded pile back into the main card deck.

        Returns None
        """

        random.shuffle(self.discarded)
        self.cards.extend(self.discarded)
        self.discarded = []

    def check_cards(self, amount):
        """
        Checks to make sure that the deck enough cards to accomodate drawing
        <amount> of cards. If not, and card exist in the discard pile, it'll
        add those cards back into the deck.

        amount: int
        """

        if (len(self.cards) < amount) and self.discarded:
            self.add_discarded()

    def cut(self, position=0):
        """
        Cuts the deck at position - 1. The second half of the deck is placed
        on top on the deck. If the position is too high or too low, the deck
        will be cut in half.
        """

        if position == 0 or position <= 0 or position >= len(self.cards)-1:
            position = len(self.cards / 2)

        back = self.cards[position:]
        self.cards = self.cards[:position]
        self.cards = back.extend(self.cards)

    def discard_from_bottom(self, amount):
        """
        Discards cards from the bottom of the deck.
            amount: int
        """

        discard = self.cards[-amount:]
        self.cards = [card for card in self.cards if card not in discard]
        self.discarded.extend(discard)

    def discard_from_hand(self, card):
        """
        Takes cards and checks if they are in self.in_hands. If they are, moves
        them into self.discarded.
        """

        if isinstance(card, Card):
            card = [card]

        cards = [x for x in self.in_hand if x in card]

        if not cards:
            return

        self.discarded.extend(cards)
        self.in_hand = [x for x in self.in_hand if x not in cards]

    def discard_from_middle(self, amount):
        """
        Discards cards from the middle of the deck.
        """

        discard_position = int(len(self.cards) / 2)
        discard = self.cards[discard_position: discard_position + amount]
        self.cards = [card for card in self.cards if card not in discard]
        self.discarded.extend(discard)

    def discard_from_deck_randomly(self, amount):
        """
        Discards cards from the deck randomly.
        """

        discard = [self.random_card() for _ in range(amount)]
        self.cards = [card for card in self.cards if card not in discard]
        self.discarded.extend(discard)

    def discard_from_top(self, amount):
        """
        Discards the specified amount of cards from the top of the deck.
        """

        discard = self.cards[:amount]
        self.cards = [card for card in self.cards if card not in discard]
        self.discarded.extend(discard)

    def draw(self, amount=1):
        """
        Draws a specified amount of cards from the deck. If the deck would run
        out of cards and cards exist in self.discarded, it will call
        self.add_discarded, self.shuffle, and continue trying to deal cards. If
        no cards can be drawn, it will return an empty list.

        draw(amount: int)

        Returns a str list.
        """

        self.check_cards(amount)

        if not self.cards:
            return []

        # Check if we need more cards than are available
        if len(self.cards) < amount and not self.discarded:
            drawn_cards = self.cards

        drawn_cards = self.cards[0:amount]
        self.in_hand.extend(drawn_cards)
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
            self.in_hand.remove(card)
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

        self.check_cards(1)

        if not self.cards:
            return ""

        card = random.choice(self.cards)
        self.cards.remove(card)
        self.in_hand.append(card)
        return card

    def reset(self):
        """
        Resets the deck to a clean state and prepares cards for use by
        shuffling the cards.
        """

        self.cards = self.clean_deck[:]
        self.discarded = []
        self.in_hand = []
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

        if isinstance(card, Card):
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

        if isinstance(card, Card):
            self.place_card(card, len(self.cards)+1)

        elif isinstance(card, list):
            if len(card) == 1:
                self.place_card(card, len(self.cards+1))
            else:
                self.place_cards(card, len(self.cards)+1)


class StandardDeck(Deck):
    def __init__(self):
        cards = ["ace", "two", "three", "four", "five", "six", "seven",
                 "eight", "nine", "ten", "jack", "queen", "king"]

        hearts = [f"{card} of hearts" for card in cards]
        diamonds = [f"{card} of diamonds" for card in cards]
        clubs = [f"{card} of clubs" for card in cards]
        spades = [f"{card} of spades" for card in cards]

        cards = []
        for i in range(13):
            if i + 1 > 10:
                worth = 10
            else:
                worth = i + 1

            cards.append(Card(name=hearts[i], worth=worth))
            cards.append(Card(name=diamonds[i], worth=worth))
            cards.append(Card(name=clubs[i], worth=worth))
            cards.append(Card(name=spades[i], worth=worth))

        super().__init__(cards)


class UnoDeck(Deck):
    def __init__(self):
        # this will need to be redone to work with the actual card objects
        # before I use this.
        double_cards = ["zero", "one", "two", "three" "four", "five", "six",
                        "seven", "eight", "nine", "draw_two", "reverse",
                        "skip"]
        colors = ["blue", "green", "red", "yellow"]
        quad_cards = ["draw four", "wild"]
        quad_cards = [[card, card, card, card] for card in quad_cards]
        cards = quad_cards[0]
        cards.extend(quad_cards[1])

        for card in double_cards:
            for color in colors:
                cards.append(f"{card} {color}")
                cards.append(f"{card} {color}")

        super().__init__(cards)
