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

        if self.character.karma:

            self.character.karma -= 1
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
        if karma_cost > self.character.karma:
            return None
        else:
            self.character.karma -= karma_cost
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

        attr = parsed.attribute[0]
        attr = attr.lower()
        attr = self.attr_abbreviations[attr]
        mod = int(parsed.modify)
        return await self.character.set_attribute_modifier(attr, mod)

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

    async def roll_damage(self, parsed):
        """
        Rolls damage against a threshold
        """

        parsed = await self.prepare_namespace(parsed)
        roll = await self.roll_attribute(parsed)
        return await roll.roll()

    async def stage_damage(self, damage_stage, roll=None):
        """
        Stages damage. If no roll is passed in, then it returns the damage
        """

        damage_types = ["l", "m", "s", "d"]
        damage_dict = {
            "l": 1,
            "m": 3,
            "s": 5,
            "d": 10
        }

        if not roll:
            return damage_dict[damage_stage]

        current_stage = damage_types.index(damage_stage)
        print(roll.result)
        hits = [hit for hit in roll.result if hit >= roll.threshold]
        current_stage -= (len(hits) // 2)
        return damage_dict[damage_types[current_stage]]

    async def handle_damage(self, parsed):
        """
        Checks damage for thresholds, damage types, and passes off to the
        appropriate condition modifier.
        """

        threshold = None
        try:
            damage_stage = int(parsed.damage)
        except ValueError:
            threshold, damage_stage = await self.get_damage(parsed.damage)

        if threshold:
            parsed.threshold = threshold
            roll = await self.roll_damage(parsed)
            damage = await self.stage_damage(damage_stage, roll)
        else:
            damage = await self.stage_damage(damage_stage)

        if parsed.stun:
            return await self.modify_stun(damage)
        elif parsed.physical:
            return await self.modify_physical(damage)

    async def get_damage(self, damage_code):
        """
        There are 2 distinct ways damage can be passed in

        threshold + damage stage: (6D, 5L, 7S, etc)
        damage stage: (L, M, S, D)

        Returns both the threshold and the damage code. The threshold will be
        None if only the damage stage is passed in.
        """

        threshold = None
        damage = None

        damage_types = ["l", "m", "s", "d"]

        damage_code = damage_code.lower()
        if len(damage_code) == 1:
            if damage_code in damage_types:
                damage = damage_code
        else:
            # We assume the last item is the damage code
            try:
                damage = damage_code[-1].lower()
                threshold = damage_code[:-1]
                threshold = int(threshold)
            except ValueError:
                return None, None

        return threshold, damage

    async def modify_stun(self, damage):
        """
        Modifies the character's stun track
        """

        await self.character.modify_stun_condition(damage)
        return self.character.condition

    async def modify_physical(self, damage):
        """
        Modifies the charcater's physical stun track
        """
        await self.character.modify_physical_condition(damage)
        return self.character.condition

    async def handle_args(self, parsable):
        try:
            parsed = await self.parse(parsable)
        except SystemExit:
            return None

        if parsed.command == "roll":
            return await self.handle_roll(parsed)
        elif parsed.command == 'skill':
            return await self.handle_skill(parsed)
        elif parsed.command == 'attribute':
            return await self.handle_attributes(parsed)
        elif parsed.command == "condition":
            return await self.handle_condition(parsed)
        else:
            print("Not yet handled")

    async def handle_attributes(self, parsed):
        if parsed.override:
            return await self.override_attribute(parsed)
        elif parsed.modifier:
            return await self.set_attribute_modifier(parsed)
        elif parsed.set:
            return await self.set_attribute(parsed)
        elif parsed.modify:
            return await self.modify_attribute(parsed)

    async def handle_condition(self, parsed):
        if parsed.damage:
            await self.handle_damage(parsed)

        return self.character.condition

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
