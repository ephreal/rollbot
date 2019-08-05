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


from . import deck
from . import player


class CardGameHandler():
    """
    The card game handler handles giving cards to players and receiving cards
    back from players, keeps track of who has what cards, and player turn
    order.

    Class Variables

        current_player (int):
            An int representing which player is currently considered the
            active player in self.players and is able to play cards.

        deck (deck.Deck):
            A deck object that represents a deck to pull cards from, place
            cards into, etc.

        players (list[player.CardPlayer]):
            A list of players in the game. Entry into this list also determines
            turn order.

        self.reverse (Boolean):
            A boolean that defines whether or not turn order is going in
            reverse. If True, players will be chosen in reverse order.

    Class Functions

        add_player(player.CardPlayer):
            Add a player to the game by using a players.CardPlayer object

        construct_and_add_player(name: str, id: unique_id, hand: list[str]):
            Creates a player object to add to self.players

        deal(amount : int, player: player.CardPlayer)
            Deals the specified amount of cards to the player

        get_next_player(skip: int) -> (int, player.CardPlayer):
            Gets the next player and returns a player.CardPlayer object. Skip
            is added to the calculation to allow for skipping a player (or
            several players). If self.reverse is True, the int will be
            turned into a negative int and then added in.

        remove_player_by_id(id: unique_id):
            Remove a player from self.players based on their unique id

        remove_player_by_index(index: int):
            Remove a player from self.players based on the index

        remove_player_by_name(name: str):
            Removes a player from self.players based on their name

        set_current_player_by_id(player_id: unique_id):
            Sets the current player based on the player id

        set_current_player_by_index(player_index: int):
            Sets the current player based on the index in self.players

        set_current_player_by_name(player_name: str):
            Sets the current player based on the player name
    """

    def __init__(self, deck=deck.StandardDeck(), players=[]):
        """
        deck:
            A deck object

        players:
            A dictionary of player names to player_info mapping.
            {"player_name" : player.CardPlayer}
        """
        self.deck = deck
        self.players = players
        self.current_player = 0
        self.reverse = False

    def add_player(self, new_player):
        """
        Adds a player to the game using a player.CardPlayer object.
        This inserts the player at the last point in the turn order.

        new_player: players.CardPlayer
        """
        self.players.append(new_player)

    def construct_and_add_player(self, name, id, hand=[]):
        """
        They always said I couldn't make my own friends to play with. Well I'll
        show THEM!

        Builds a player.CardPlayer object and adds the player to the end of
        the players list

        name: str
            Players name

        id: unique identifier. Can be anything provided it's unique

        hand: list[str]
            A list of cards that will be placed in the player's hand
        """

        new_player = player.CardPlayer(name=name, id=id, hand=hand)

        self.players.append(new_player)

    def deal(self, amount, to_player):
        """
        Deals the specified amount of cards to the player.

        amount: int

        to_player: player.CardPlayer

        Returns a string list of cards
        """

        cards = self.deck.draw(amount)
        to_player.hand.extend(cards)
        return cards

    def deal_by_id(self, amount, player_id):
        """
        Deals the specified amount of cards via player id

        amount: int
        player_id: unique_id

        Returns a string list if the player exists, otherwise returns None
        """

        player_id = [
            player for players in self.players if player.id == player_id
        ]
        player_id = player_id[0]

        if player_id:
            cards = self.deal(amount, player_id)
            return cards
        else:
            return None

    def deal_by_name(self, amount, player_name):
        """
        Deals the specified amount of cards to the player (by name):

        amount: int
        player_name: str
        """
        pass

    def get_next_player(self, skip=0):
        """
        Gets the next player. If skip is defined, skip will be added to the
        calculation to determine who the next player is.

        If self.reverse is True, then the next player will be selected in
        reverse the normal order.

        skip: int
            How many players to skip. Default 0.
        """

        if self.reverse:
            next_player = -1
            if skip:
                skip = 0 - skip

        else:
            next_player = 1

        next_player += skip

        next_player += self.current_player

        next_player %= len(self.players)

        return (next_player, self.players[next_player])

    def remove_player_by_id(self, id):
        """
        Removes a player based on their id

        id: Unique ID.
        """

        self.players = [
            player for player in self.players if not player.id == id
        ]

    def remove_player_by_index(self, index):
        """
        Removes a player based on the index provided. Any number larger than
        len(self.players) will be modded down to fit.

        index: int
        """

        index %= len(self.players)

        self.players.pop(index)

    def remove_player_by_name(self, name):
        """
        Removes a player from the game based on their name

        name: str
        """

        self.players = [
            player for player in self.players if not player.name == name
        ]

    def set_current_player_by_id(self, player_id):
        """
        Sets the current player based on the player id
        """

        player = [player for player in self.players if player.id == player_id]

        self.current_player = self.players.index(player[0])

    def set_current_player_by_index(self, player_index):
        """
        Sets the current player based on the index in self.players
        """

        self.current_player = player_index % len(self.players)

    def set_current_player_by_name(self, player_name):
        """
        Sets the current player based on the player name
        """

        player = [
            player for player in self.players if player.name == player_name
        ]

        self.current_player = self.players.index(player[0])


class BlackjackHandler(CardGameHandler):
    """
    Class Variables

        current_winner(int):
            An integer pointing to the current highest (but below 22) player

        current_ties(player.BlackjackPlayer):
            A list of players with the same total score as self.highest_score

        dealer (player.BlackjackPlayer):
            The dealer of cards. Always goes last.

        highest_score (int):
            An int that is the largest tally seen so far

    Class Functions

        check_tally(player: player.BlackjackPlayer):
            Checks the player's tally against the high score.

        dealer_play():
            The super simple ruleset that the dealer will play by. This will
            be improved in the future. For now, good enough.

        double_hit(card_player: player.BlackjackPlayer):
            Gives the player "card_player" 2 more cards to their hand.

        hit(card_player: player.BlackjackPlayer):
            Give the player "card_player" 1 more card to their hand.

        setup():
            Gives every player their cards

        stand():
            Increments the current_player counter

        stay():
            alias for stand. Included because some prefer the term stay to
            stand.
    """
    def __init__(self):
        self.dealer = player.BlackjackPlayer(name="dealer", hand=[], id=0)
        super().__init__(deck=deck.StandardDeck(), players=[self.dealer])

        # dealer always goes last, so point this at the next player
        self.current_player += 1
        self.highest_score = 0
        self.current_winner = None
        self.current_ties = []

    def check_tally(self, card_player):
        """
        Checks to make sure that the card_player's tally isn't above or equal
        to the current high score.
        """

        if card_player.tally > self.highest_score and card_player.tally < 22:
            self.current_winner = self.players.index(card_player)
            self.highest_score = card_player.tally
            self.current_ties = [card_player]

        elif card_player.tally == self.highest_score:
            self.current_ties.append(card_player)

    def construct_and_add_player(self, name, id, hand=[]):
        """
        Overriding the base class function to use player.BlackjackPlayer
        """

        new_player = player.BlackjackPlayer(name=name, id=id, hand=hand)
        self.add_player(new_player)

    def dealer_play(self):
        """
        The logic used to guide the program through making an intelligent
        choice when it plays the game with others.
        """

        if self.dealer.tally >= 17:
            self.stand()

        if self.dealer.tally < 9:
            self.double_hit(self.dealer)
        else:
            while self.dealer.tally < 17:
                self.hit(self.dealer)

    def double_hit(self, card_player):
        """
        Gives two cards to card_player. Wrapper for deal function.

        card_player: player.CardPlayer
        """

        cards = self.deal(2, card_player)
        card_player.receive_cards(cards)

        self.check_tally(card_player)

        return cards

    def hit(self, card_player):
        """
        Gives a single card to a player. Wrapper for deal function.

        card_player: player.CardPlayer
        """

        card = self.deal(1, card_player)
        card_player.receive_card(card[0])

        self.check_tally(card_player)

        return card

    def setup(self):
        """
        Sets up the blackjack game by dealing two cards to the player(s) and to
        the "dealer", in this case, the bot.

        Currently, this only knows how to play with a single player. Additional
        players will be added in the future.
        """

        [self.double_hit(card_player) for card_player in self.players]

    def stand(self):
        """
        Indicates that a player is finished with his or her turn. Increments
        the current_player counter.
        """

        self.current_player += 1
        self.current_player %= len(self.players)

    def stay(self):
        """
        Convenience function that calls self.stand() as some people use the
        phrase "stay" instead of "stand".
        """

        self.stand()
