# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

from utils.rpg.abc import character_abc
from utils.rolling.handlers import Sr3RollHandler


class SR3Character(character_abc.CharacterABC):
    __slots__ = ("name", "race", "sex", "age", "description", "notes",
                 "attributes", "skills", "karma", "gear", "cyberwear",
                 "spells", "condition", "contacts", "handler")

    def __init__(self, **kwargs):

        self.name = kwargs.pop("name", None)
        self.race = kwargs.pop("race", None)
        self.sex = kwargs.pop("sex", None)
        self.age = kwargs.pop("age", None)
        self.description = kwargs.pop("description", None)
        self.notes = kwargs.pop("notes", None)
        self.attributes = kwargs.pop("attributes", None)
        self.skills = kwargs.pop("skills", None)
        self.karma = kwargs.pop("karma", None)
        self.gear = kwargs.pop("gear", None)
        self.cyberwear = kwargs.pop("cyberwear", None)
        self.spells = kwargs.pop("spells", None)
        self.condition = kwargs.pop("condition", None)
        self.contacts = kwargs.pop("contacts", None)
        self.handler = Sr3RollHandler()

    async def get_skill(self, skill):
        """
        Gets a skill. Throws a KeyError if the attribute does not exist
        """
        try:
            return self.skills[skill]
        except KeyError:
            skill_keys = list(self.skills.keys())
            for skill_name in skill_keys:
                specializations = self.skills[skill_name]['specializations']
                specialization_names = list(specializations.keys())
                for specialization_name in specialization_names:
                    if skill == specialization_name:
                        skill = specializations[skill]
                        break

        return skill

    async def roll_attribute(self, attribute, threshold=4):
        attribute = await self.get_attribute(attribute)
        attr_name = list(attribute.keys())[0].capitalize()
        roll = [str(threshold), "-n", "rolling", f"{attr_name[0]}"]

        try:
            if attribute['override']:
                roll = roll.insert(0, attribute['override'])
            else:
                total = attribute['base'] + attribute['modifier']
                roll = roll.insert(0, str(total))
            return await self.handler.roll(roll)
        except KeyError:
            total = attribute['base'] + attribute['modifier']
            roll.insert(0, str(total))
            return await self.handler.roll(roll)

    async def roll_skill(self, skill, threshold=4):
        skill = await self.get_skill(skill)
        skill_name = list(skill.keys())[0].capitalize()
        roll = [str(skill['level']), str(threshold), "-n",
                f"roll for {skill_name}"]
        return await self.handler.roll(roll)

    async def roll_spell(self, spell_name, threshold):
        """
        Currently rolls the character's sorcery skill if it exists. In the
        future, this will also return things like damage staging.
        """
        return await self.roll_attribute('sorcery')
