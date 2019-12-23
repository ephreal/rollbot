# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

from . import game_handler
from . import player
from . import states

import random


class DiscordInterface():
    """
    Provides an interface to rapptz's discord.py to allow for

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

            create_game(game_type: str, initial_player: discord.member):
            -> session_id: int
                Handles the initial creation of the game with the initial
                player.

            create_game_handler(game_type: str, session_id: int):
                Create a game handler based on the contents of game_type.
                Defaults to game_handler.BlackjackHandler

            generate_session() -> int:
                Generates a game_session_id for use with add_game_handler.

            get_game_state_by_member(discord.member) -> states.GameState:
                returns a game state object for ease of use in discord

            make_player(member: discord.member object):
                Creates and returns a CardPlayer object
    """
    def __init__(self):
        self.current_players = {}
        self.current_sessions = {}

    async def add_game_handler(self, game_type):
        """
        Generates a game_session_id and adds the handler to the
        current_sessions dict. The players will be added to the current_players
        dict with an active state of False.

        handler: game_handler
            Can be any valid game handler from game_handler.py

        return: session_id (int)
        """

        session_id = self.generate_session()
        await self.create_game_handler(game_type, session_id)

        return session_id

    async def add_player_to_current_players(self, new_player, sid):
        """
        Adds a player to the session passed in.

        new_player: discord.member
        sid: int
            -> None
        """
        # For now, I'm going to get the game handler to handle all the player
        # creation and leave the rest up to you because it is getting late.
        # This required changes on all of the following:
        #   add_player_to_game (Commented out a line)
        #   create_game
        #   pass_commands (Removed passing through player object)
        self.current_players[new_player.id] = {
                                               "session_id": sid,
                                               "in_game": False,
                                               "member": new_player
                                               }

    async def add_players_to_current_players(self, players, sid):
        """
        Adds a list of players to a game session

        players: list[member]

        sid: int
        """

        for new_player in players:
            await self.add_player_to_current_players(new_player)

    async def add_player_to_game(self, new_player):
        """
        Sets a player as active in the session the session they are mapped to.

        new_player: discord member
        """

        self.current_players[new_player.id]["in_game"] = True

    async def add_players_to_game(self, players):
        """
        Sets a list of players as active in the game session they are mapped to

        players: list[discord member]
        """

        for member in players:
            await self.add_player_to_game(member)

    async def create_game(self, game_type, initial_player):
        """
        Handles the initial creation of the game with the initial
        player.

        game_type: str
        initial_player: discord.member
            -> session_id: int
        """

        session_id = await self.add_game_handler(game_type)
        handler = self.current_sessions[session_id]
        await handler.construct_and_add_player(
            name=initial_player.name,
            player_id=initial_player.id,
            discord_member=initial_player
        )
        await self.add_player_to_current_players(initial_player, session_id)
        await self.add_player_to_game(initial_player)
        return session_id

    async def create_game_handler(self, game_type, session_id):
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

    async def get_game_state_by_member(self, member):
        """
        Builds and returns a states.GameState object for discord.

        returns states.GameState
        """

        session = self.current_players[member.id]["session_id"]
        handler = self.current_sessions[session]

        game_state = states.GameState(session, handler)
        await game_state.set_current_player()

        return game_state

    async def is_playing(self, member):
        """
        Checks to see if the discord member is currently in a game.

        member: discord.member
            -> in_game: bool
        """

        return self.current_players[member.id]["in_game"]

    # NOTE: This method below is slated for removal. It makes FAR more sense
    #       to handle player creation within the game handler rather than the
    #       discord interface.
    @classmethod
    async def make_player(self, member):
        """
        Makes a player object for adding a player to the current players list.

        member: discord member object
        """

        new_player = player.CardPlayer(
                                        name=member.name,
                                        player_id=member.id,
                                        hand=[],
                                        discord_member=member
        )
        return new_player

    async def pass_commands(self, member, commands):
        """
        Passes commands onto the correct game handler for the player.

        member: discord.member
        commands: list[str]
            -> response: str
        """

        player_dict = self.current_players[member.id]
        handler = self.current_sessions[player_dict["session_id"]]
        current_player = await handler.get_player_by_id(member.id)
        return await handler.handle_commands(current_player, commands)

    async def remove_player_from_game(self, member):
        """
        Sets the player as not active in a game.

        member: discord.member
            -> None
        """

        game_player = self.current_player[member.id]
        game_player["in_game"] = False

    async def start_game(self, sid):
        """
        Starts the game specified by the session id.

        sid: int
            -> None
        """

        await self.current_sessions[sid].setup()
