# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

from utils.rolling.rolling_utils import roll


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

        self.result = await roll(self.dice, self.sides)
