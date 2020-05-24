# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

from utils.rpg.abc import character_abc


class SR3Character(character_abc.CharacterABC):
    __slots__ = ("name", "race", "sex", "age", "description", "notes",
                 "attributes", "skills", "karma", "gear", "cyberware",
                 "spells", "condition", "contacts", "handler", "career")

    def __init__(self, **kwargs):

        character = kwargs.pop("character", None)
        self.name = character.pop('name', None)
        self.race = character.pop('race', None)
        self.sex = character.pop('sex', None)
        self.age = character.pop('age', None)
        self.description = character.pop('description', None)
        self.notes = character.pop('notes', None)
        self.career = character.pop('career', None)
        self.karma = character.pop('karma', None)

        self.attributes = kwargs.pop("attributes", None)
        self.skills = kwargs.pop("skills", None)
        self.gear = kwargs.pop("gear", None)
        self.cyberware = kwargs.pop("cyberware", None)
        self.spells = kwargs.pop("spells", None)
        self.condition = kwargs.pop("condition", None)
        self.contacts = kwargs.pop("contacts", None)

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

    async def modify_karma(self, karma):
        """
        Verifies karma does not drop below 0 when being modified
        """

        if self.karma + karma < 0:
            raise ValueError

        else:
            self.karma += karma
            if karma > 0:
                self.career['karma'] += karma

        return self.karma

    async def modify_base_attribute(self, attribute, modifier):
        """
        Modifies a base attribute safely
        """

        attribute = self.get_attribute(attribute)
        if attribute['base'] + modifier < 0:
            raise ValueError

        attribute['base'] += modifier
        return attribute

    async def set_attribute_modifier(self, attribute, modifier):
        """
        Sets the attribute modifier to the modifier passed in
        """

        attribute = await self.get_attribute(attribute)
        attribute['modifier'] = modifier
        return attribute

    async def set_attribute_override(self, attribute, override):
        """
        Sets the attribute override to the override passed in
        """
        attribute = self.get_attribute(attribute)
        attribute['override'] = override
        return attribute
