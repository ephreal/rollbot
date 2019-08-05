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

from . import game_handler
from . import player
from . import deck


class GameBase():
    """"
    Base card game class to create card games from

    Class Variables

        handler (game_handler.CardGameHandler):
            The card game handler to use. By default, creates a standard
            52 card deck handler.

    Class functions

        GameBase.Deal(amount : int, player : player.CardPlayer) -> list[str]:
            Deals a specified amount of cards to a player. Returns
            the cards as a list.
    """
    def __init__(self, card_deck=None):
        if not card_deck:
            self.deck = deck.standard_deck()
        else:
            self.deck = card_deck

        self.handler = game_handler.CardGameHandler(deck=self.deck, players=[])

    def deal(self, amount, to_player):
        """
        Deals a specified amount of cards to the player passed in.

        amount: int

        to_player: player.CardPlayer
        """

        cards = self.deck.draw(amount)
        player.hand.extend(cards)

        return cards

    def
