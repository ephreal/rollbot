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


from . import base_roll_functions


class Shadowrun1Roller():
    """
    The shadowrun roller for shadowrun 1E games.

    class methods:
        roll(dice_pool: int) -> list[int]
            Rolls and counts the dice according to shadowrun 1E rules. Does
            no checks for failures or successes. Returns a list of integers
            representing the totals.
            SR1E CORE pg. 20-21

        check_successes(target: int, rolls: list[int])
                -> dict(int, list[int], Boolern)
            Checks how many integers in the rolls list exceed the target int.
            Returns a dictionary with the amount of successes and the integers
            that exceeded the target and whether or not the roll is a failure
            SR1E CORE pg. 21-22

        initiative(dice_pool: int, modifier: int) -> initiative: int
            Rolls initiative dice and adds in reaction to give the initiative
            score.
            SR1E CORE pg. 62

        is_failure(rolls: list[int]) -> Boolean
            Checks to see if the roll is a failure, which is all 1's by
            shadowrun 1E rules. Returns True if the roll is a failure.
            SR1E CORE pg. 20-21
    """

    def __init__(self):
        self.roller = base_roll_functions.roller()

    async def roll(self, dice_pool):
        """
        Rolls and counts the dice according to shadowrun 1E rules. This does
        no checking for successes.

        dice_pool : int

            -> list[int]
        """

        rolls = await self.roller.roll(dice_pool)

        if 6 in rolls:
            # Get the sixes and remove them from the original list.
            sixes = [x for x in rolls if x == 6]
            rolls = [x for x in rolls if x != 6]
            added = await self.roll(len(sixes))
            sixes = [sixes[i] + added[i] for i in range(0, len(sixes))]
            rolls.extend(sixes)

        return rolls

    async def check_successes(self, target, rolls):
        """
        Checks the rolls to see if any of the rolls are successes

        target : int
        roll : list[int]

            -> dict{successes: int, rolls[int], failure: Bool}
        """

        rolls = [roll for roll in rolls if roll > target]

        successes = {"successes": len(rolls),
                     "rolls": rolls
                     }

        if await self.is_failure(rolls):
            successes["failure"] = True
        else:
            successes["failure"] = False

        return successes

    async def roll_initiative(self, dice_pool=1, modifier=1):
        """
        Rolls initiative dice and adds reaction in.

        dice_pool: int
        reaction: int

            -> int
        """

        # Adding 6's does not apply to initiative. Therefore use the general
        # roller.
        initiative = await self.roller.roll(dice_pool)
        for i in initiative:
            modifier += i

        return modifier

    async def is_failure(self, rolls):
        """
        Checks to see if the roll is a failure. This is only the case if all
        items in the roll are a 1.

        rolls : list[int]

            -> bool
        """

        ones = [x for x in rolls if x == 1]
        if len(ones) == len(rolls):
            return True

        return False


class Shadowrun5Roller():
    """
    TODO: Add in glitch counting.

    The shadowrun roller is my handler for all shadowrun 5E related rolling
    functions. Types of rolls that are completed inlcude

    general rolling and hit counting
        - Adding in additional dice with +
        - removing dice with -

    class variables:
        roller (base_roll_functions.roller()):
            A roller class that handles the actual dice rolling.

    class methods:

        basic_rolling(dice_pool: int, exploding: Boolean) -> list[int]:
            A dice roller that handles basic dice rolling. This allows for
            exploding 6's with exploding=True
            SR5E CORE pg. 44
            SR5E CORE pg. 56 (EDGE) push the limit before/after rolling

        buy_hits(dice_pool: int) -> hits: int
            "buys" hits at a 1 hit : 4 dice ratio. Rounds down.
            SR5E CORE pg. 45

        count_hits(rolls: list[int], prime: Boolean) -> {hits, misses, ones}
            Creates the amount of hits, misses, and ones in the rolls. If the
            roll is designated for a prime runner, it lowers the hit threshold
            by 1.
            SR5E CORE pg. 44

        extended_test(dice_pool: int, threshold: int, prime: boolean)
            -> {success: bool, hits: list[ {hits: int, list[int]} ]}
            Runs extended tests by shadowrun 5E rules. Stops as soon as
            the test has been completed rather than running through all
            iterations if not needed.
            SR5E CORE pg. 48

        initiative_roll(dice_pool: int, modifier: int) -> initiative: int
            Rolls initiative for shadowrun 5E.
            SR5E CORE pg. 159
    """
    def __init__(self):
        self.roller = base_roll_functions.roller()

    async def roll(self, dice_pool, exploding=False):
        """
        A dice roller that handles basic dice rolling. This allows for
        exploding 6's with exploding=True

        dice_pool: int
        exploding: Boolean

<<<<<<< HEAD
<<<<<<< HEAD
            -> list[int]
=======
        returns: ([rolls].sorted(), hits, misses, ones)
>>>>>>> 68173db0ef9685c7d7e72c87ed400bb7563871e8
=======
        returns: ([rolls].sorted(), hits, misses, ones)
>>>>>>> 68173db0ef9685c7d7e72c87ed400bb7563871e8
        """

        rolls = await self.roller.roll(dice_pool=dice_pool, sides=6)
        if exploding:
            sixes = [x for x in rolls if x == 6]
            rolls.extend(await self.roll(len(sixes)))
            rolls.sort()
            return rolls

        rolls.sort()
        return rolls

    async def buy_hits(self, dice_pool=0):
        """
        "buys" hits at a 1 hit : 4 dice ration. Rounds down.

        dice_pool: int

            -> int
        """

        return dice_pool // 4

    async def count_hits(self, rolls, prime=False):
        """
        Counts the amount of hits, misses, and ones in a list of integers.

        rolls: list[int]

            -> {hits, misses, ones}
        """

        hit_limit = 5
        # Lower the hit threshold if rolling for a prime runner
        if prime:
            hit_limit = 4

        hits, misses, ones = 0, 0, 0
        for i in rolls:
            if i >= hit_limit:
                hits += 1
            elif i > 1:
                misses += 1
            else:
                ones += 1

        return {"hits": hits, "misses": misses, "ones": ones}

    async def extended_test(self, dice_pool, threshold, prime=False):
        """
        Runs an extended test with a dice pool to see if it is possible to
        reach a threshold. Prime will lower the threshold when counting hits
        if it is True. Returns a dict with a boolean representing success
        status and a list of int lists representing the rolls.

        dice_pool: int
        threshold: int
        prime: False

            -> {success, list[ {hits: int, list[int]} ]}
        """

        rolls = []
        totals = []
        success = False
        total_hits = 0
        while dice_pool > 0:
            roll = await self.roll(dice_pool)

            if prime:
                counted = await self.count_hits(roll, prime=True)
            else:
                counted = await self.count_hits(roll)

            total_hits += counted["hits"]
            totals.append(total_hits)
            rolls.append({"hits": counted["hits"], "roll": roll})

            dice_pool -= 1

            if total_hits >= threshold:
                success = True
                break

        return {"success": success, "rolls": rolls, "totals": {
                                    "total_hits": total_hits,
                                    "running_total": totals}}

    async def roll_initiative(self, dice_pool, modifier=0):
        """
        Rolls initiative for shadowrun 5E.

        dice_pool: int
        modifier: int

            -> initiative: int
        """

        initiative_roll = await self.roll(dice_pool)
        for i in initiative_roll:
            modifier += i

        return modifier
