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
                 "attributes", "skills", "karma", "gear", "cyberwear",
                 "spells", "condition", "contacts")

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

    def roll_attribute(self, attribute, mod):
        print("attributes, woo")

    def roll_skill(self, skill, mod):
        print("skills, woo")
