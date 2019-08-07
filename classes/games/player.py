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


class Player():
    """
    A base player class to be extended and made into something beautiful.

    Class Variables
        player_name (str):
            The player's name.
        player_id (int):
            The player's ID for the session. In the case of discord, this
            will be a discord.member object to allow direct messaging.
    """

    def __init__(self, name=None, id=None):
        self.name = name
        self.id = id


class CardPlayer(Player):
    """
    Represents a player in a card game.

    Class variables

        hand (list[card.Card]):
            A list of all cards currently in the player's hand

    Class Functions

        add_card_to_hand(card: card.Card):
            Adds the given card to the CardPlayer's hand

        add_cards_to_hand(cards: list[card.Card]):
            Adds the given cards to the CardPlanyer's hand

        remove_card_from_hand(card: card.Card):
            Removes the given card from the CardPlayer's hand

        remove_cards_from_hand(card: card.Card)
            Removes the given cards from the CardPlayer's hand
    """

    def __init__(self, hand=[], name=None, id=None):
        super().__init__(name, id)
        self.hand = hand

    def __str__(self):
        """
        Returns the player's name
        """
        return f"{self.name}"

    def add_card_to_hand(self, card):
        """
        Adds the given card to the player's hand

        card: card.Card
        """

        self.hand.append(card)

    def add_cards_to_hand(self, cards):
        """
        Adds the given cards to the player's hand

        cards: list[card.Card]
        """

        self.hand.extend(cards)

    def remove_card_from_hand(self, card):
        """
        Removes the given card from the player's hand

        card: card.Card
        """

        self.hand.remove(card)

    def remove_cards_from_hand(self, cards):
        """
        Removes the given cards from the players hand

        cards: list[str]
        """

        self.hand = [card for card in self.hand if card not in cards]


class BlackjackPlayer(CardPlayer):
    """
    Automatically sets a few extra variables needed for playing blackjack

    Additional Class Variables:

        bust (Boolean)
            States whether a player is bust or not

        tally (int)
            A running tally of the player's hand.

    Additional Class Functions

        receive_card(card, card.Card):
            Increases tally by card.worth

        receive_cards(cards: list[card.Card]):
            Increases tally by both cards' worth
    """
    def __init__(self, hand=[], name=None, id=None):
        super().__init__(hand=hand, name=name, id=id)

        self.bust = False
        self.tally = 0

    def receive_card(self, card):
        """
        Adds card to self.hand and adds card.value to self.tally. If self.tally
        becomes larger than 21, it sets self.bust to True

        card: card.Card
        """

        self.tally += card.worth

        if self.tally > 21:
            self.bust = True

    def receive_cards(self, cards):
        """
        Receives multiple cards and adds them to self.hand and increases
        self.tally by the cards' self.worth.

        Calls self.receive_card() twice to make this happen

        cards: list[card.Card]
        """

        self.receive_card(cards[0])
        self.receive_card(cards[1])
