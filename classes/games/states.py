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


class GameState():
    """
    Allows for easy use of all game state on discord.

    Class Variables

        These variables are all stored in other classes, the game state makes
        running the game in discord far easier, ie, this way you don't need
        to do a long twisted discord_handler.current_sessions[session].......
        in order to have a player draw a card.

        cards_in_hand (list[card]):
            A list of all cards currently in player's hands

        current_player (player.*):
            The current player in this game

        handler (game_handler.*):
            The handler for this particular game

        session_id (int):
            The ssession ID the game is part of

        valid_commands (list[str]):
            A list of valid commands for this game
    """

    def __init__(self, session, game_handler):
        self.session_id = session
        self.handler = game_handler

        self.cards_in_hand = self.handler.deck.in_hand
        self.current_player = self.handler.get_current_player()
        self.valid_commands = self.handler.expose_commands()
