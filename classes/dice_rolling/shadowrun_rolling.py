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

import base_roll_functions


class Shadowrun5Roller():
    """
    The shadowrun roller is my handler for all shadowrun 5E related rolling
    functions. Types of rolls that are completed inlcude

    general rolling and hit counting
        - Adding in additional dice with +
        - removing dice with -

    class variables:
        roller (base_roll_functions.roller()):
            A roller class that handles the actual dice rolling.

    class methods:

        basic_rolling(dice_pool: int):
            A basic roller that rolls dice_pool amount of dice and passes the
            dice around to be counted for hits, checked for glitches, etc.
    """
    def __init__(self):
        self.roller = base_roll_functions.roller()

    def basic_rolling(self, dice_pool):
        """
        A dice roller that handles basic dice rolling. The dice hits are
        counted, glitches are checked for, and the result is returned as a
        (hits, misses, ones) set.

        dice_pool: int

        returns: (hits, misses, ones)
        """

        rolls = await self.roller.roll(dice_pool=dice_pool, sides=6)
        rolls.sort()
        counted_rolls = self.count_hits(rolls)

    def count_hits(self, rolls, prime=False):
        """
        A function that counts the amount of hits, misses, and ones in a list
        of integers.

        rolls: list[int]

        returns: (hits, misses, ones)
        """

        # Lower the hit threshold if rolling for a prime runner
        if prime:
            hit_limit = 4
        else:
            hit_limit = 5

        hits, misses, ones = 0
        hits = [hits+1 for roll in rolls if roll >= hit_limit]
        misses = [misses+1 for roll in rolls if roll >= 1 and
                  roll <= hit_limit]
        ones = [ones+1 for roll in rolls if roll == 1]
