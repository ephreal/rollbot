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

        message = ["```md"]
        message.append(f"Result: {sum(self.result) + self.mod}")
        message.append("="*len(message[1]))
        message.append(f"> Rolls: {self.result}")
        message.append(f"Roll: {sum(self.result)}")
        message.append(f"Modifier: {self.mod}")
        if self.note:
            message.append(f"< Note: {' '.join(self.note)} >")
        message.append("```")

        return "\n".join(message)

    async def roll(self):
        """
        Makes a roll with XdY dice
        """

        self.result = await rolling_utils.roll(self.dice, self.sides)


class DndRoll(BaseRoll):
    def __init__(self, dnd_roll):
        super().__init__(dnd_roll)
        self.adv = dnd_roll.adv
        self.dis = dnd_roll.dis

    async def format(self):
        message = ["```md"]
        if self.adv:
            message = await self.format_advantage(message)
        elif self.dis:
            message = await self.format_disadvantage(message)
        else:
            message = await self.general_format(message)

        if self.note:
            message.append(f"< Note: {' '.join(self.note)} >")

        message.append("```")
        return "\n".join(message)

    async def format_advantage(self, message):
        """
        Formats a roll with advantage
        """
        mod = self.dice
        self.sides = 20
        self.dice = 2
        await self.roll()

        message.append("< Advantage >")
        message.append(f"Result: {max(self.result) + mod}")
        message.append("="*len(message[-1]))
        message.append(f"> Rolls: {self.result}")
        message.append(f"Highest: {max(self.result)}")
        message.append(f"Mod: {mod}")
        return message

    async def format_disadvantage(self, message):
        """
        Formats a roll with advantage
        """
        mod = self.dice
        self.sides = 20
        self.dice = 2
        await self.roll()

        message.append("< Disadvantage >")
        message.append(f"Result: {min(self.result) + mod}")
        message.append("="*len(message[-1]))
        message.append(f"> Rolls: {self.result}")
        message.append(f"Lowest: {min(self.result)}")
        message.append(f"Mod: {mod}")
        return message

    async def general_format(self, message):
        """
        General roll formatting
        """

        await self.roll()

        message.append(f"Result: {sum(self.result) + self.mod}")
        message.append("="*len(message[-1]))
        message.append(f"> Rolls: {self.result}")
        message.append(f"Total: {sum(self.result)}")
        message.append(f"Modifier: {self.mod}")
        return message


class Sr3Roll(BaseRoll):
    def __init__(self, sr3_roll):
        super().__init__(sr3_roll)
        # shadowrun is all D6's
        self.sides = 6
        self.threshold = sr3_roll.threshold
        self.initiative = sr3_roll.initiative
        self.open = sr3_roll.open
        if self.mod:
            self.threshold -= self.mod

    async def format(self):
        """
        Formats the roll for SR3E rolls. This includes thresholds, hits, ones,
        and results
        """

        if not self.result:
            await self.roll()

        message = ["```md"]
        if self.initiative:
            message = await self.initiative_formatting(message)
        elif self.open:
            message = await self.open_test_formatting(message)
        else:
            message = await self.general_formatting(message)
        if self.note:
            message.append(f"< Note: {' '.join(self.note)} >")

        message.append("```")

        return "\n".join(message)

    async def open_test_formatting(self, message):
        """
        Formats a roll for an open test
        """

        highest = 0
        for roll in self.result:
            if roll > highest:
                highest = roll
        message.append(f"Open Test Threshold: {highest}")
        message.append("="*len(message[1]))
        message.append(f"> Rolls: {self.result}")
        return message

    async def initiative_formatting(self, message):
        """
        Formats a roll for an initiative roll
        """
        too_high = [6 for x in self.result if x > 6]
        result = [x for x in self.result if x <= 6]
        result.extend(too_high)
        self.result = result
        message.append(f"Initiative: {sum(self.result) + self.initiative}")
        message.append("="*len(message[1]))
        message.append(f"> Rolls: {self.result}")
        message.append(f"Total: {sum(self.result)}")
        message.append(f"Modifier: {self.initiative}")
        return message

    async def general_formatting(self, message):
        """
        Formatts a roll for a general test
        """
        if len(self.ones) == self.dice:
            message.append("< CRITICAL FAILURE >")
        elif not self.hits:
            message.append("< FAILURE >")
        message.append(f"Hits: {len(self.hits)}")
        message.append("="*len(message[-1]))
        message.append(f"> Rolls: {self.result}")
        message.append(f"Threshold: {self.threshold}")
        return message

    async def roll(self):
        """
        Rolls dice with a SR3E dice roller.
        """
        self.result = await rolling_utils.sr3_roll(self.dice, self.sides)
        self.result.sort()
        self.hits = [x for x in self.result if x >= self.threshold]
        self.ones = [x for x in self.result if x == 1]
