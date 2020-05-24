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

    async def modify_karma(self, karma):
        """
        Verifies karma does not drop below 0 when being modified
        """
        if self.race == 'human':
            pool_update = 10
        else:
            pool_update = 20

        if self.karma['good'] + karma < 0:
            raise ValueError

        else:
            self.karma['good'] += karma
            if karma > 0:
                self.karma['total'] += karma

        if (self.karma["total"] % pool_update) == 0 and (
           not self.karma['total'] == 0):
            self.karma['pool'] += 1

        return self.karma
