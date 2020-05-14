# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

from utils.rolling import rolling_utils


class BaseRoll:
    """
    Sets up a roll namespace for ease of use
    """

    def __init__(self, base_roll):
        self.dice, self.sides = self.check_dice(base_roll.dice)
        self.note = base_roll.note
        self.mod = base_roll.mod
        self.result = None

    def check_dice(self, dice):
        """
        dice: String in the format XdY
        """
        # default roll type is 1d20
        default = (1, 20)

        if not dice:
            return default

        if "d" not in dice.lower():
            try:
                dice = int(dice)
                return (dice, 20)
            except ValueError:
                return (1, 20)
        else:
            amount, sides = dice.lower().split("d")
            try:
                amount = int(amount)
                sides = int(sides)
            except ValueError:
                amount = 1
                sides = 20
            return (amount, sides)
        return default

    async def format(self):
        """
        Formats the roll for ease of returning a message
        """

        if not self.result:
            await self.roll()

        message = []
        message.append(f"You rolled {self.dice}, {self.sides}-sided dice")
        message.append(f"Result: {sum(self.result) + self.mod} "
                       f"({sum(self.result)} + {self.mod})")
        message.append(f"Modifier: {self.mod}")
        message.append(f"Rolls: {self.result}")
        if self.note:
            message.append(f"Note: {' '.join(self.note)}")

        return "\n".join(message)

    async def roll(self):
        """
        Makes a roll with XdY dice
        """

        self.result = await rolling_utils.roll(self.dice, self.sides)


class Sr1Roll(BaseRoll):
    def __init__(self, sr1_roll):
        super().__init__(sr1_roll)
        # shadowrun is all D6's
        self.sides = 6
        self.threshold = sr1_roll.threshold
        self.initiative = sr1_roll.initiative
        if self.mod:
            self.threshold -= self.mod

    async def format(self):
        """
        Formats the roll for SR1E rolls. This includes thresholds, hits, ones,
        and results
        """

        if not self.result:
            await self.roll()

        message = []
        message.append(f"You rolled {self.dice} six-sided dice")
        if self.initiative:
            message.append(f"Initiative: {sum(self.result) + self.initiative}"
                           f" ({sum(self.result)} + {self.initiative})")
        else:
            if len(self.ones) == self.dice:
                message.append("CRITICAL FAILURE")
            elif not self.hits:
                message.append("FAILURE")
            message.append(f"Total hits: {len(self.hits)}")
            message.append(f"Threshold: {self.threshold}")
        message.append(f"Rolls: {self.result}")
        if self.note:
            message.append(f"Note: {' '.join(self.note)}")

        return "\n".join(message)

    async def roll(self):
        """
        Rolls dice with a SR1E dice roller.
        """
        self.result = await rolling_utils.sr1_roll(self.dice, self.sides)
        self.result.sort()
        self.hits = [x for x in self.result if x >= self.threshold]
        self.ones = [x for x in self.result if x == 1]
