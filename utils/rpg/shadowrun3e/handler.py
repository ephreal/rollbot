# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""


from utils.rpg.shadowrun3e import parser
from utils.rolling import rolls
import json


__all__ = ("SR3CharacterHandler")


class SR3CharacterHandler():
    def __init__(self, character=None):
        self.parser = parser.Sr3CharacterParser
        self.character = character
        self.attr_abbreviations = {
            "b": "body",
            "c": "charisma",
            "i": "intelligence",
            "q": "quickness",
            "s": "strength",
            "w": "willpower",
        }

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

    async def prepare_attribute(self, parsed):
        """
        Prepars an attribute for rolling, modification, etc
        """
        if not parsed.attribute:
            raise ValueError

        try:
            attribute = parsed.attribute.lower()
            attribute = self.attr_abbreviations[attribute[0]]
            attribute = await self.character.get_attribute(attribute)
        except KeyError:
            return None

        return attribute

    async def roll_attribute(self, parsed):
        """
        Creates a roll object and returns it
        """

        attribute = await self.prepare_attribute(parsed)
        if not attribute:
            return None

        if attribute['override']:
            total = attribute['override']
        else:
            total = attribute['base'] + attribute['modifier']

        parsed.dice = str(total)
        parsed = await self.prepare_namespace(parsed)
        roll = rolls.Sr3Roll(parsed)
        return roll

    async def roll_skill(self, parsed):
        """
        Creates a roll object and returns it
        """

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

    async def add_skill(self, parsed):
        """
        Adds a skill to the character.

        Currently this reads in a list of skills from a json file. They will be
        fetched from a database in the future.
        """

        with open("utils/rpg/shadowrun3e/skills.json", "r") as f:
            skills = json.loads(f.read())

        if self.character.karma['good']:

            self.character.karma['good'] -= 1
            skill = parsed.skill.lower()
            self.character.skills[skill] = skills[skill]
            self.character.skills[skill]['level'] = 1
            self.character.skills['specializations'] = {}
            return skills[skill]

        return None

    async def modify_skill(self, parsed):
        """
        Modifies a character's skill. If the value is positive, the character
        must have enough karma to cover the cost. Decreases in skill are
        free.
        """

        skill = await self.character.get_skill(parsed.skill.lower())
        if not skill:
            return None

        attribute = await self.character.get_attribute(skill['attribute'])
        value = int(parsed.modify)
        base = attribute['base']

        karma_cost = await self.calculate_skill_karma(value, skill, base)
        if karma_cost > self.character.karma['good']:
            return None
        else:
            self.character.karma['good'] -= karma_cost
            skill["level"] += value
            return skill

    async def calculate_skill_karma(self, modifier, skill, base):
        """
        Calculates the karma cost to modify a skill.

        0 if modifier is <= 0
        1.5 * modifier (round down) if modifier <= base
        2 * modifier (round down) if modifier <= 2 * base
        2.5 * modifier (round down) if modifier > 2 * base
        """

        # Casting to int here to round down
        if modifier < 0:
            return 0

        elif modifier <= base:
            return int(1.5 * modifier)

        elif modifier <= (2 * base):
            return 2 * modifier

        elif modifier > (2 * base):
            return int(2.5 * modifier)

    async def set_attribute_modifier(self, parsed):
        """
        Sets the attribute modifier
        """

        attribute = await self.prepare_attribute(parsed)
        if not attribute:
            return None

        attribute['modifier'] = int(parsed.modifier)
        return attribute

    async def set_attribute(self, parsed):
        """
        Sets the attribute to the value parsed
        """

        attribute = await self.prepare_attribute(parsed)
        if not attribute:
            return None

        if int(parsed.modify) > -1:
            attribute['base'] = int(parsed.modify)
        return attribute

    async def modify_attribute(self, parsed):
        """
        Modifies an attribute if the character has it
        """
        attribute = await self.prepare_attribute(parsed)
        if not attribute:
            return None

        # Ensure an attribute can never be below 0
        if not attribute['base'] + int(parsed.modify) < 0:

            attribute['base'] += int(parsed.modify)
            return attribute

    async def override_attribute(self, parsed):
        """
        Sets the override on an attribute
        """
        attribute = await self.prepare_attribute(parsed)
        if not attribute:
            return None

        attribute['override'] = int(parsed.override)
        return attribute

    async def modify_karma(self, parsed):
        """
        Modify's the character's karma
        """

        return await self.character.modify_karma(int(parsed.karma))

    async def handle_args(self, parsable):
        parsed = await self.parse(parsable)
        if parsed.command == "roll":
            return await self.handle_roll(parsed)
        elif parsed.command == 'skill':
            return await self.handle_skill(parsed)
        elif parsed.command == 'attribute':
            return await self.handle_attributes(parsed)
        else:
            print("Not yet handled")

    async def handle_attributes(self, parsed):
        if parsed.modify and not parsed.set:
            return await self.modify_attribute(parsed)
        elif parsed.override:
            return await self.override_attribute(parsed)
        elif parsed.modifier:
            return await self.set_attribute_modifier(parsed)
        elif parsed.set:
            return await self.set_attribute(parsed)

    async def handle_roll(self, parsed):
        if parsed.attribute:
            return await self.roll_attribute(parsed)
        elif parsed.skill:
            return await self.roll_skill(parsed)
        elif parsed.spell:
            return await self.roll_spell(parsed)
        else:
            return None

    async def handle_skill(self, parsed):
        if parsed.add:
            return await self.add_skill(parsed)
        elif parsed.modifier:
            return await self.modify_skill(parsed)
