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

from . import game_handler
from . import player
import random


class DiscordInterface():
    """
    Provides an interface to rapptz discord.py to allow for

        - Automatic mapping of disord users to an ongoing game
          (Assuming they are playing a game, of course)
        - Simultaneous games on the same server/multiple servers
        - Use of discord.py context/member objects to access correct game
          session

        All this is made possible by using the discord.py context object.

        Thanks rapptz, the rewrite of your discord library is amazing.

        Class Variables:

            current_players ( { name : { ctx.member,
                                         session_id,
                                         in_game} }  )
                A dictionary of all currently playing members and the session
                id. If the player is currently playing a game, in_game is True.

            current_sessions ({game_session_id : [game_handler,
                                                  game_channel] })
                A dict containing session id's mapped to game handlers. The
                game_channel is the ctx.channel that the game was initiated
                from.

        Class Functions

            add_game_handler(game_type: str):
                Generates a game_session_id and adds the handler to the
                current_sessions list. game_type is a string name of the game.

            add_player_to_current_players(player: ctx.member, sid: int):
                Adds a player to the current_players dict. If they are
                already in the list and not in_game, their session_id will
                be overwritten with the new one.

            add_players_to_current_players(players: list[member],
                                           sid: int):
                Adds the players in the players list to the current_players
                dictionary. If a player is already in the list and not in_game,
                their current session_id will be overwritten with the new one.

            add_player_to_game(player: member):
                Adds a player to the game_handler their session_id points to.

            add_players_to_game(players: list[member]):
                Adds multiple players to the game_handler their session_id
                points to.

            create_game_handler(game_type: str, session_id: int):
                Create a game handler based on the contents of game_type.
                Defaults to game_handler.BlackjackHandler

            generate_session() -> int:
                Generates a game_session_id for use with add_game_handler.
    """
    def __init__(self):
        self.current_players = {}
        self.current_sessions = {}

    def add_game_handler(self, game_type):
        """
        Generates a game_session_id and adds the handler to the
        current_sessions dict. The players will be added to the current_players
        dict with an active state of False.

        handler: game_handler
            Can be any valid game handler from game_handler.py
        """

        session_id = self.generate_session()
        self.create_game_handler(game_type, session_id)

    def add_player_to_current_players(self, new_player, sid):
        """
        Adds a player to the session passed in.

        new_player: member

        sid: int
        """

        player_obj = self.make_player(new_player)
        self.current_players[new_player.id] = {"player": player_obj,
                                               "session_id": sid,
                                               "in_game": False,
                                               "member": new_player
                                               }

    def add_players_to_current_players(self, players, sid):
        """
        Adds a list of players to a game session

        players: list[member]

        sid: int
        """

        for new_player in players:
            self.add_player_to_current_players(new_player)

    def add_player_to_game(self, new_player):
        """
        Sets a player as active in the session the session they are mapped to.

        new_player: discord member
        """

        player_session = self.current_players[new_player.id]["session_id"]
        player_obj = self.current_players[new_player.id]["player_obj"]

        self.current_sessions[player_session].add_player(player_obj)
        self.current_players[new_player.id]["in_game"] = True

    def add_players_to_game(self, players):
        """
        Sets a list of players as active in the game session they are mapped to

        players: list[discord member]
        """

        for member in players:
            self.add_player_to_game(member)

    def create_game_handler(self, game_type, session_id):
        """
        Creates a game handler for use in add_game_handler based on the content
        of game_type.

        Defaults to game_handler.BlackjackHandler

        game_type: str

        session_id: int
        """

        if game_type.lower().startswith("b"):
            handler = game_handler.BlackjackHandler()

        # Currently I have no other games to add.
        else:
            handler = game_handler.BlackjackHandler()

        self.current_sessions[session_id] = handler

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

    def make_player(self, member):
        """
        Makes a player object for adding a player to the current players list.

        member: discord member object
        """

        new_player = player.CardPlayer(
                                        name=member.name,
                                        player_id=member.id,
                                        hand=[]
        )
        return new_player
