# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""


from utils.rolling import rolling_utils


class Shadowrun3Roller():
    """
    The shadowrun roller for shadowrun 1E games.

    class methods:

        check_successes(target: int, rolls: list[int])
                -> dict(successes: int, rolls: list[int], failure: bool)
            Checks how many integers in the rolls list exceed the target int.
            Returns a dictionary with the amount of successes and the integers
            that exceeded the target and whether or not the roll is a failure

        is_failure(rolls: list[int]) -> bool
            Checks to see if the roll is a failure, which is all 1's by
            shadowrun 1E rules. Returns True if the roll is a failure.

        roll(dice_pool: int) -> list[int]
            Rolls and counts the dice according to shadowrun 1E rules. Does
            no checks for failures or successes. Returns a list of integers
            representing the totals.

        roll_initiative(dice_pool: int, modifier: int) -> initiative: int
            Rolls initiative dice and adds in reaction to give the initiative
            score.
    """

    def __init__(self):
        pass

    async def check_successes(self, target, rolls):
        """
        Checks the rolls to see if any of the rolls are successes

        target : int
        roll : list[int]

            -> dict{successes: int, rolls[int], failure: Bool}
        """

        rolls = [roll for roll in rolls if roll >= target]

        successes = {"successes": len(rolls),
                     "rolls": rolls
                     }

        if await self.is_failure(rolls):
            successes["failure"] = True
        else:
            successes["failure"] = False

        return successes

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

    async def roll(self, dice_pool):
        """
        Rolls and counts the dice according to shadowrun 1E rules. This does
        no checking for successes.

        dice_pool : int

            -> list[int]
        """

        rolls = await rolling_utils.roll(dice_pool)

        if 6 in rolls:
            # Get the sixes and remove them from the original list.
            sixes = [x for x in rolls if x == 6]
            rolls = [x for x in rolls if x != 6]
            added = await self.roll(len(sixes))
            sixes = [sixes[i] + added[i] for i in range(0, len(sixes))]
            rolls.extend(sixes)

        return rolls

    async def roll_initiative(self, dice_pool=1, modifier=1):
        """
        Rolls initiative dice and adds reaction in.

        dice_pool: int
        reaction: int

            -> int
        """

        # Adding 6's does not apply to initiative. Therefore use the general
        # roller.
        initiative_roll = await rolling_utils.roll(dice_pool)
        for i in initiative_roll:
            modifier += i

        return initiative_roll, modifier


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

        buy_hits(dice_pool: int) -> hits: int
            "buys" hits at a 1 hit : 4 dice ratio. Rounds down.
            SR5E CORE pg. 45

        count_hits(rolls: list[int], prime: Boolean) -> {hits, misses, ones}
            Creates the amount of hits, misses, and ones in the rolls. If the
            roll is designated for a prime runner, it lowers the hit threshold
            by 1.
            SR5E CORE pg. 44

        extended_test(dice_pool: int, threshold: int, prime: boolean)
            -> {success: bool, rolls: list[int], totals {total_hits: int,
                running_total: list[int]}}
            Runs extended tests by shadowrun 5E rules. Stops as soon as
            the test has been completed rather than running through all
            iterations if not needed.
            SR5E CORE pg. 48

        is_glitch(rolls: list[int], hits: int)
            -> {glitch: bool, type: str or None}
            Checks whether or not a roll is a glitch.
            SR5E CORE pg. 45-46

        roll(dice_pool: int, exploding: Boolean) -> list[int]:
            A dice roller that handles basic dice rolling. This allows for
            exploding 6's with exploding=True
            SR5E CORE pg. 44
            SR5E CORE pg. 56 (Edge effects)

        roll_initiative(dice_pool: int, modifier: int) -> initiative: int
            Rolls initiative for shadowrun 5E.
            SR5E CORE pg. 159
    """
    def __init__(self):
        pass

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

    async def extended_test(self, dice_pool, threshold, prime=False,
                            exploding=False):
        """
        Runs an extended test with a dice pool to see if it is possible to
        reach a threshold. Prime will lower the threshold when counting hits
        if it is True. Returns a dict with a boolean representing success
        status and a list of int lists representing the rolls.

        dice_pool: int
        threshold: int
        prime: bool
        exploding: bool

            -> {success, rolls, totals {total_hits, running_total}}
        """

        rolls = []
        totals = []
        success = False
        total_hits = 0
        while dice_pool > 0:
            roll = await self.roll(dice_pool, exploding=exploding)

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

    async def is_glitch(self, rolls, hits):
        """
        Checks whether or not a roll is a glitch.

        rolls: list[int]
        hits: int

            -> dict{glitch: bool, type: str or None}
        """

        glitch = False
        glitch_type = None

        ones = [x for x in rolls if x == 1]

        if len(ones) > (len(rolls) // 2) and not hits:
            glitch = True
            glitch_type = "critical"

        elif len(ones) > (len(rolls) // 2) and hits:
            glitch = True
            glitch_type = "normal"

        return {"glitch": glitch, "type": glitch_type}

    async def roll(self, dice_pool, exploding=False):
        """
        A dice roller that handles basic dice rolling. This allows for
        exploding 6's with exploding=True

        dice_pool: int
        exploding: Boolean

            -> list[int]
        """

        rolls = await rolling_utils.roll(dice_pool=dice_pool, sides=6)
        if exploding:
            sixes = [x for x in rolls if x == 6]
            rolls.extend(await self.roll(len(sixes)))
            rolls.sort()
            return rolls

        rolls.sort()
        return rolls

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

        return initiative_roll, modifier
