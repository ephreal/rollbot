# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""


class Player():
    """
    A base player class to be extended and made into something beautiful.

    Class Variables
        discord_member:
            The discord.py member object to allow direct messaging of a player
        player_id (int):
            The player's ID for the session.
        player_name (str):
            The player's name.

    Class Methods
        send(message: str) -> None
            Sends a private message to the player.
    """

    def __init__(self, discord_member=None, name=None, player_id=None):
        self.discord_member = discord_member
        self.id = player_id
        self.name = name

    def send(self, message):
        """
        Sends a private message to the player.

        message: str
            -> None
        """

        self.discord_member.send(message)


class CardPlayer(Player):
    """
    Represents a player in a card game.

    Class variables

        hand (list[card.Card]):
            A list of all cards currently in the player's hand

    Class Functions

        add_cards_to_hand(cards: list[card.Card]):
            Adds the given cards to the CardPlayer's hand

        remove_card_from_hand(card: card.Card):
            Removes the given card from the CardPlayer's hand

        remove_cards_from_hand(card: card.Card)
            Removes the given cards from the CardPlayer's hand
    """

    def __init__(self, discord_member=None, hand=[], name=None,
                 player_id=None):
        super().__init__(discord_member, name, player_id)
        self.hand = hand

    def __str__(self):
        """
        Returns the player's name
        """
        return f"{self.name}"

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

        split_hand (list[Card])
            The secondary hand that a player has when they choose to split.

    Additional Class Functions

        add_cards_to_hand(cards: list[card.Card]) -> None:
            Overwritten function to properly handle additional things that
            must happen when adding a card to a blackjack player's hand

        can_split(): -> bool
            Checks whether or not a player is allowed to split their hand.
            Returns True if both cards in the player's hand are the same value.

        check_bust(): -> None
            Tallys up the player's current hand(s) to see if they have gone
            bust or not.
    """
    def __init__(self, discord_member=None, hand=[], name=None,
                 player_id=None, split_hand=None):
        super().__init__(discord_member=discord_member, hand=hand, name=name,
                         player_id=player_id)

        self.bust = False
        self.split_hand = split_hand
        self.tally = 0

    def add_cards_to_hand(self, cards):
        """
        Overwriting super method to extend this functionality.
        Adds the given cards to the player's hand and immediately updates some
        class variables to be sane.

        cards: list[card.Card]
        """

        self.hand.extend(cards)
        self.check_bust()

    def check_bust(self):
        """
        Checks the player's hand(s) to see if the player has gone bust or not
            -> None
        """
        self.tally = self.count_hand(self.hand)

        # Player's card value is above 21 and has no split hand
        if self.tally > 21 and not self.split_hand:
            self.bust = True

        # Player has a split hand
        if self.split_hand:
            if self.count_hand(self.split_hand) > 21:
                self.bust = True
            else:
                self.swap_hands()
                self.tally = self.count_hand(self.hand)

    def count_hand(self, hand):
        """
        Counts the total value of a hand.

        hand: list[card.Card]
            -> value: int
        """

        self.tally = 0
        for card in hand:
            self.tally += int(card)

        return self.tally

    async def split(self):
        """
        Splits the player's hand into 2 hands.

            -> None
        """

        self.split_hand = self.hand[0:1]
        self.hand = self.hand[1:]

    async def swap_hands(self):
        """
        Changes the self.split_hand to be self.hand. Only needed when a player
        has split their hand an want's to draw cards for the other hand.

            -> None
        """

        temp = self.split_hand
        self.split_hand = self.hand
        self.hand = temp
