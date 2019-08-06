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
import random


class DiscordInterface():
    """
    Provides an interface to rapptz discord.py to allow for

        - Automatic mapping of disord users to an ongoing game
            + (Assuming they are playing a game, of course)
        - Simultaneous games on the same server/multiple servers
        - Use of discord.py context object to access correct game session

        All this is made possible by using the discord.py context object.

        Thanks rapptz, the rewrite of your discord library is amazing.

        Class Variables:

            current_players ( {ctx.member : [game_session_id,
                                             active,
                                             in_game}  )
                A dictionary of all currently playing members and the session
                id. If they are active, they have responded to the request to
                play the game. If the player is currently playing a game,
                in_game returns True.

            current_sessions ({game_session_id : [game_handler,
                                                  game_channel] })
                A dict containing session id's mapped to game handlers. The
                game_channel is the ctx.channel that the game was initiated
                from.

        Class Functions

            add_game_handler(handler: game_handler,
                             players: list[ctx.member]):
                Generates a game_session_id and adds it to the current_sessions
                list. It'll add the players to the "current_players" dict for
                ease of session mapping if they accept. Their active state
                will be set to false.

            add_player_to_current_players(player: ctx.member, sid: int):
                Adds a player to the current_players dict. If they are
                already in the list and not in_game, their session_id will
                be overwritten with the new one.

            add_players_to_current_players(players: list[ctx.member],
                                           sid: int):
                Adds the players in the players list to the current_players
                dictionary. If a player is already in the list and not in_game,
                their current session_id will be overwritten with the new one.

            add_player_to_game(player: ctx.member):
                Adds a player to the game_handler their session_id points to.

            add_players_to_game(players: list[ctx.member]):
                Adds multiple players to the game_handler their session_id
                points to.

            create_game_handler(game_type: str) -> game_handler.*:
                Create a game handler based on the contents of game_type.
                Defaults to game_handler.BlackjackHandler

            generate_session() -> int:
                Generates a game_session_id for use with add_game_handler.
    """
    def __init__(self):
        self.current_players = {}
        self.current_sessions = {}

    def add_game_handler(self, handler, players=None):
        """
        Generates a game_session_id and adds the handler to the
        current_sessions dict. The players will be added to the current_players
        dict with an active state of False.

        handler: game_handler
            Can be any valid game handler from gane_handler.py

        players: list[ctx.member]
            A list of member objects resolved from ctx.guild.members or
            ctx.guild.get_member()
        """

        if not players:
            return

        session_id = self.generate_session()
        self.current_sessions[session_id] = handler

        self.add_players_to_current(players, session_id)

    def add_player_to_current_players(new_player, sid):
        """
        Adds a player to the session passed in.

        new_player: player.*

        sid: int
        """

        pass

    def add_players_to_game_current_players(players, sid):
        """
        Adds a list of players to a game session

        players: list[player.*]

        sid: int
        """

        pass

    def add_player_to_game(new_player):
        """
        Sets a player as active in the session the session they are mapped to.

        new_player: player.*
        """

        pass

    def add_players_to_game(players):
        """
        Sets a list of players as active in the game session they are mapped to

        players: list[player.*]
        """

        pass

    def create_game_handler(self, game_type):
        """
        Creates a game handler for use in add_game_handler based on the content
        of game_type.

        Defaults to game_handler.BlackjackHandler

        game_type: str

        returns a game_handler.* object.
        """

        if game_type.lower().startswith("b"):
            handler = game_handler.BlackjackHandler()

        # Currently I have no other games to add.
        else:
            handler = game_handler.BlackjackHandler()

        return handler

    def generate_session(self):
        """
        Generates a random game session for use. If the game session id is
        already in use, it'll try generate another one.

        returns int
        """

        session_id = None
        while session_id is None or (
                            session_id in (self.current_sessions.keys())):
            session_id = random.randint(10000000000, 99999999999)

        return session_id
