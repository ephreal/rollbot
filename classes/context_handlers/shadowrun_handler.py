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


from classes.dice_rolling import shadowrun_rolling as sr
from classes.formatters import shadowrun_formatter as sf


class ShadowrunHandler():
    def __init__(self):
        self.edition = 5
        self.roller = sr.Shadowrun5Roller()
        self.formatter = sf.Shadowrun5Formatter()
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

    async def set_sr_edition(self, edition):
        """
        Sets the current shadowrun edition to the specified edition. If that
        edition is not present, nothing changes.

        edition: int
        """

        if edition == 1:
            self.roller = sr.Shadowrun1Roller()
            self.formatter = sf.Shadowrun1Formatter()
            self.edition = 1
        elif edition == 5:
            self.roller = sr.Shadowrun5Roller()
            self.formatter = sf.Shadowrun1Formatter()
            self.edition = 5

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

    async def extended_test(self, dice_pool, threshold, prime=False):
        """
        Runs an extended test. Currently only available for 5E

        dice_pool: list[int]
        threshold: int
        prime: bool

            -> extended_test{}
        """

        extended_test = self.roller.extended_test(dice_pool, threshold, prime)
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

    async def roll_initiative(self, dice_pool, modifier):
        """
        Rolls initiative with the current handler and returns it.

        dice_pool: int
        modifier: int

            -> initiative: int
        """

        return await self.roller.roll_initiative(dice_pool, modifier)

    async def format_initiative(self, initiative):
        """
        Returns a formatted string for ease of reading in discord.

        initiative: int

            -> formatted_initiative: str
        """

        return await self.formatter.format_initiative(initiative)

    async def sr5_is_glitch(self, rolls, hits):
        """
        Gets whether or not a roll is a glitch according to sr5 rules

        rolls: list[int]
        hits: int

            -> {glitch: bool, type: str}
        """

        return await self.roller.is_glitch(rolls, hits)
