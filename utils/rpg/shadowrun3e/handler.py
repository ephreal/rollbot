# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""


from utils.rpg.shadowrun3e import parser
from utils.rolling import rolls


__all__ = ("SR3CharacterHandler")


class SR3CharacterHandler():
    def __init__(self, character=None):
        self.parser = parser.Sr3CharacterParser
        self.character = character

    async def parse(self, parsable):
        return self.parser.parse_args(parsable)

    async def prepare_namespace(self, namespace):
        """
        Prepares a namespace for use with a roll.
        """

        namespace.mod = 0
        namespace.initiative = None
        namespace.open = None
        return namespace

    async def roll_attribute(self, parsable_list):
        """
        Creates a roll object and returns it
        """

        parsed = await self.parse(parsable_list)
        if not parsed.attribute:
            raise ValueError

        abbreviations = {
            "b": "body",
            "c": "charisma",
            "i": "intelligence",
            "q": "quickness",
            "s": "strength",
            "w": "willpower",
        }

        try:
            attribute = parsed.attribute.lower()
            attribute = abbreviations[attribute[0]]
            attribute = await self.character.get_attribute(attribute)
        except KeyError:
            return None

        if attribute['override']:
            total = attribute['override']
        else:
            total = attribute['base'] + attribute['modifier']

        parsed.dice = str(total)
        parsed = await self.prepare_namespace(parsed)
        roll = rolls.Sr3Roll(parsed)
        return roll

    async def roll_skill(self, parsable_list):
        """
        Creates a roll object and returns it
        """

        parsed = await self.parse(parsable_list)
        if not parsed.skill:
            raise ValueError

        try:
            skill = parsed.skill.lower()
            skill = await self.character.get_skill(skill)
        except KeyError:
            return None

        # This is a kludgy hack and needs to be fixed tomorrow when I'm awake.
        try:
            parsed.dice = str(skill['level'])
        except TypeError:
            return None

        parsed = await self.prepare_namespace(parsed)
        roll = rolls.Sr3Roll(parsed)
        return roll
