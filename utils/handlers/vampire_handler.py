# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

from utils.handlers.shadowrun_handler import BaseHandler
from utils.rolling import parsers


class VampireMasqueradeHandler(BaseHandler):
    """
    Vampire the Masquerade handler that provides an interface for all rolling.
    """

    def __init__(self):
        super().__init__()
        self.parser = parsers.VampireMasqueradeParser()

    async def check_roll(self, roll, threshold=6):
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
        checked: {successes, rolls, failure}
        verbose: Bool

            -> formatted_roll: str
        """

        return await self.formatter.format_roll(roll, checked, verbose=verbose)

    async def roll(self, dice_pool):
        """
        Rolls dice_pool 10d6.

        dice_pool: int

            -> list[int]
        """

        return await self.roller.roll(dice_pool, 10)
