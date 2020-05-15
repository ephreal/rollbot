# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""


class Shadowrun3Formatter():
    """
    class methods:
        format_roll(rolls: list[int], checked: dict, verbose: bool,
            glitch: dict or None)
        -> formatted_roll: str
            Formats 3E rolls to easily identify successes and failures.

        format_initiative(initiative: int) -> formatted_initiative: str
            Formats the initiative score to be easier to understand in discord.
    """

    def __init__(self):
        pass

    async def format_roll(self, rolls, checked, verbose=False, glitch=None):
        """
        Formats 3E rolls to easily identify successes and failures.
        """

        if checked["failure"]:
            formatted_rolls = "TEST FAILED\n"
        else:
            formatted_rolls = "Test succeeded\n"

        formatted_rolls += f"You rolled {len(rolls)} dice\n"\
                           f"You had {checked['successes']} successes.\n\n" \
                           f"successes: {checked['successes']}\n" \
                           f"failures: {len([x for x in rolls if x == 1])}"

        if verbose:
            formatted_rolls += f"\n\nrolls: {rolls}\n"\

        return formatted_rolls

    async def format_initiative(self, roll, initiative, verbose=False):
        """
        Formats the initiative score to be easier to understand in discord.

        initiative: int

            -> Formatted initiative: str
        """

        formatted = f"Your initiative score is {initiative}"
        if verbose:
            formatted += f"\nRolls: {roll}"

        return formatted

    async def format_unchecked_roll(self, roll):
        """
        Formats a roll that has not been checked.

        roll: list[int]

            -> formatted_roll: str
        """

        return f"You rolled {len(roll)} dice\nRoll: {roll}"


class Shadowrun5Formatter():
    """
    class methods:
        format_roll(rolls: list[int], counted: dict, verbose: bool,
        glitch: bool) -> formatted_roll: str
            Formats 5E rolls to easily identify hits, misses, and ones, and
            glitches in discord.
            If verbose is True, the dice rolls are added to the result.

        format_buy_hits(bought_hits: int) -> formatted_hits: str
            Formats bought hits to be easily understandable in discord.

        format_extended_test(extended_test: dict) -> formatted_test: str
            Formats an extended test to be easily understandable in discord.

        format_initiative(initiative) -> formatted_initiative: str
            Formats and initiative roll to be easily understandable in discord.
    """

    def __init__(self):
        pass

    async def format_roll(self, rolls, counted, verbose=False, glitch=None):
        """
        Formats 5E rolls to easily identify hits, misses, and ones, and
        glitches in discord.
        If verbose is True, the dice rolls are added to the result.

        rolls: list[int]
        counted: {hits: int, misses: int, ones: int}
        glitch: {glitch: bool, type: str}

            -> formatter_rolls: str
        """

        formatted_rolls = ""

        if glitch is not None:
            if glitch['glitch']:
                formatted_rolls += f"A {glitch['type']} glitch occured!\n"

        formatted_rolls += f"You rolled {len(rolls)} dice.\n"\
                           f"hits   : {counted['hits']}\n"\
                           f"misses : {counted['misses']}\n"\
                           f"ones   : {counted['ones']}"

        if verbose:
            formatted_rolls += f"\nRolls  : {rolls}"

        return formatted_rolls

    async def format_buy_hits(self, bought_hits):
        """
        Formats bought hits to be easily understandable in discord.

        bought_hits: int

            -> formatted_hits: int
        """

        return f"You bought {bought_hits} hits."

    async def format_extended_test(self, extended_test):
        """
        Formats an extended test to be easily understandable in discord.

        extended_test: {success, rolls, {total_hits, running_total}}

            -> formatted_extened_test: str
        """

        if extended_test['success']:
            formatted = "Test successfully completed.\n"
        else:
            formatted = "Test failed.\n"
        formatted += f"Total hits: {extended_test['totals']['total_hits']}\n\n"

        rolls = extended_test['rolls']
        totals = extended_test['totals']['running_total']

        for i in range(0, len(totals)):
            formatted += f"Current: {totals[i]} roll: {rolls[i]['roll']}\n"

        return formatted

    async def format_initiative(self, roll, initiative, verbose=False):
        """
        Formats and initiative roll to be easily understandable in discord.

        initiative: int

            -> formatted_initiative: str
        """

        formatted = f"Your initiative score is {initiative}"
        if verbose:
            formatted += f"\nRolls: {roll}"

        return formatted
