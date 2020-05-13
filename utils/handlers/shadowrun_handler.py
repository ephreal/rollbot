# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""


from classes.dice_rolling import shadowrun_rolling as sr
from classes.formatters import shadowrun_formatter as sf
from utils.rolling import parsers


class BaseHandler():
    """
    A base handler that has common functions to all shadowrun games. Some will
    need to be overridden, but most should apply.

    class methods:

        add_roll(author: string, roll: list[int], checked: dict) -> None
            Adds a roll from an author to past_rolls for use if a reroll is
            needed. Any old rolls are overwritten.

        format_initiative(initiative: int) -> formatted_initiative: str
            Returns a formatted string for ease of reading in discord.

        roll_initiative(dice_pool: int, modifier: int) -> initiative: int
            Rolls initiative with the current handler and returns it.
    """

    def __init__(self):
        self.parser = parsers.BaseRollParser()
        self.past_rolls = {}

    async def add_roll(self, author, roll, checked):
        """
        Adds a roll from an author to self.past_rolls for use if a reroll is
        needed. Any old rolls are overwritten.

        author: str
        roll: list[int]
        checked: dict{hits, misses, ones}

            -> None
        """

        self.past_rolls[author] = {"roll": roll, "checked": checked}

    async def parse(self, args):
        return self.parser.parse_args(args)

    async def format_initiative(self, initiative, roll, verbose=False):
        """
        Formats the initiative roll with the formatter used in the handler.
        All formatters will accept the same format.

        initiative: int
        roll: list[int]

            -> formatted_initiative: str
        """

        return await self.formatter.format_initiative(roll, initiative,
                                                      verbose=verbose)

    async def roll_initiative(self, dice_pool, modifier):
        """
        Rolls initiative according to shadowrun 1E rules.

        dice_pool: int

            -> list[int], int
        """

        return await self.roller.roll_initiative(dice_pool, modifier)


class ShadowrunHandler(BaseHandler):
    """
    The shadowrun handler is the interface to discord for all shadowrun
    rolling.

    class methods:

        check_roll(roll: list[int], threshold: int, prime: bool)
        -> checked {} (content varies depending on SR edition)
            Checks the roll to see how many successes/failures are in the roll.
            Having a threshold is required for 1E. Setting prime = True will
            have SR5 roller lower the threshold for one when counting hits.

        extended_test(dice_pool: list[int], threshold: int, prime: bool)
        -> extended_test: {success: bool, rolls: list[int],
           totals {total_hits: int, running_total: list[int]}}
            Runs an extended test. Currently only available for 5E

        format_extended_test(extended_test: {}) -> formatted_extended_test: str
            Formats an extended test and returns a formatted string for display
            in discord.

        format_roll(roll: list[int], checked: {}, verbose: bool, glitch: bool)
        -> formatted_roll: str
            Returns a formatted string for discord using the currently
            active roll handler.

        reroll(author, prime: bool) -> reroll {}
            Allows rerolling of a past roll as per sr5 rules (all dice that did
            not make a hit)

        roll(dice_pool: int, exploding: bool)
            Rolls dice_pool amount of dice with the currently active roller.
            Returns a list of ints represesenting the rolls.

        set_sr_edition(edition: int) -> None
            Sets the current shadowrun edition to the specified edition. If the
            edition is not available, nothing changes.

        sr5_is_glitch(rolls: list[int], hits: int) -> glitch: {glitch, type}
            Gets whether or not a roll is a glitch according to sr5 rules
    """
    def __init__(self):
        super().__init__()
        self.edition = 5
        self.parser = parsers.Sr5RollParser()
        self.roller = sr.Shadowrun5Roller()
        self.formatter = sf.Shadowrun5Formatter()

    async def check_roll(self, roll, threshold=2, prime=False):
        """
        Checks the roll to see how many successes/failures are in the roll.
        Having a threshold is required for 1E. Setting prime = True will have
        SR5 roller lower the threshold for one when counting hits.

        roll: list[int]
        threshold: int
        prime: Bool

            -> SR1: {successes, rolls, failure}
            -> SR5: {hits, misses, ones}
        """

        if self.edition == 1:
            checked = await self.roller.check_successes(threshold, roll)

        elif self.edition == 5:
            checked = await self.roller.count_hits(roll, prime)

        return checked

    async def extended_test(self, dice_pool, threshold, prime=False,
                            exploding=False):
        """
        Runs an extended test. Currently only available for 5E

        dice_pool: list[int]
        threshold: int
        prime: bool
        exploding: bool

            -> extended_test{}
        """

        extended_test = self.roller.extended_test(dice_pool, threshold, prime,
                                                  exploding)
        return await extended_test

    async def format_extended_test(self, extended_test):
        """
        Formats an extended test and returns a formatted string for display in
        discord.

        extended_test: {}

            -> formatted_extended_test: str
        """

        formatted_test = self.formatter.format_extended_test(extended_test)
        return await formatted_test

    async def format_roll(self, roll, checked, verbose=False, glitch=None):
        """
        Returns a formatted string for discord using the currently
        active roll handler.

        roll: list[int]
        checked: SR1: {successes, rolls, failure}
        checked: SR5: {hits, misses, ones}
        verbose: Bool
        glitch: bool

            -> formatted_roll: str
        """

        return await self.formatter.format_roll(roll, checked, verbose, glitch)

    async def reroll(self, author, prime=False):
        """
        Allows rerolling of a past roll as per sr5 rules (all dice that did
        not make a hit)

        author: string

            -> {old: list[int], reroll: list[int],
                checked: {hits, misses, ones}
               }
        """

        old = self.past_rolls[author]
        reroll_dice = old['checked']['misses'] + old['checked']['ones']
        reroll = await self.roll(reroll_dice)
        reroll.extend(old['roll'][reroll_dice:])

        checked = await self.check_roll(reroll, prime=prime)
        await self.add_roll(author, reroll, checked)

        return {'old': old, "reroll": reroll, 'checked': checked}

    async def roll(self, dice_pool, exploding=False):
        """
        Rolls dice_pool amount of dice with the currently active roller.
        Returns a list of ints represesenting the rolls.

        dice_pool: int
        exploding: Bool

            -> list[int]
        """

        if self.edition == 1:
            roll = await self.roller.roll(dice_pool)

        elif self.edition == 5:
            roll = await self.roller.roll(dice_pool, exploding)

        return roll

    async def set_sr_edition(self, edition):
        """
        Sets the current shadowrun edition to the specified edition. If that
        edition is not available, nothing changes.

        edition: int
        """

        if edition == 1:
            self.roller = sr.Shadowrun1Roller()
            self.formatter = sf.Shadowrun1Formatter()
            self.edition = 1
        elif edition == 5:
            self.roller = sr.Shadowrun5Roller()
            self.formatter = sf.Shadowrun5Formatter()
            self.edition = 5

    async def sr5_is_glitch(self, rolls, hits):
        """
        Gets whether or not a roll is a glitch according to sr5 rules

        rolls: list[int]
        hits: int

            -> {glitch: bool, type: str}
        """

        return await self.roller.is_glitch(rolls, hits)


class Shadowrun1Handler(BaseHandler):
    """
    Shadowrun 1E handler that provides an interface to a discord bot for all
    Shadowrun 1E rolling.
    """

    def __init__(self):
        super().__init__()
        self.parser = parsers.Sr1RollParser()
        self.roller = sr.Shadowrun1Roller()
        self.formatter = sf.Shadowrun1Formatter()

    async def check_roll(self, roll, threshold=2):
        """
        Checks the roll to see how many successes/failures are in the roll.

        roll: list[int]
        threshold: int

            -> {successes, rolls, failure}
        """

        checked = await self.roller.check_successes(threshold, roll)
        return checked

    async def format_roll(self, roll, checked, verbose=True):
        """
        Returns a formatted string for discord using the currently
        active roll handler.

        roll: list[int]
        checked: SR1: {successes, rolls, failure}
        verbose: Bool

            -> formatted_roll: str
        """

        return await self.formatter.format_roll(roll, checked, verbose=verbose)

    async def format_unchecked_roll(self, roll):
        """
        Returns a formatted string for times when the roll in not checked.

        roll: list[int]
            -> formatted_roll: str
        """

        return await self.formatter.format_unchecked_roll(roll)

    async def roll(self, dice_pool):
        """
        Rolls dice according to shadowrun 1E rules.

        dice_pool: int

            -> list[int]
        """

        return await self.roller.roll(dice_pool)
