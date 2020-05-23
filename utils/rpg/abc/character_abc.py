# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

import abc
import json


class CharacterABC(abc.ABC):
    __slots__ = ()

    def __init__(self):
        pass

    async def get_attribute(self, attribute):
        """
        Gets an attribute. Throws a KeyError if the attribute does not exist.
        """
        return self.attributes[attribute]

    async def get_skill(self, skill):
        """
        Gets a skill. Throws a KeyError if the attribute does not exist
        """
        return self.skills[skill]

    async def get_spell(self, spell_name):
        """
        Gets a spell. Throws a KeyError if the attribute does not exist
        """
        return self.spells[spell_name]

    async def roll_attribute(self, attribute, modifier):
        pass

    async def roll_skill(self, skill, modifier):
        pass

    async def roll_spell(self, spell, modifier):
        pass

    async def to_dict(self):
        character = {}
        for attribute in self.__slots__:
            character[attribute] = getattr(self, attribute, None)
        return character

    @staticmethod
    async def from_json_file(subclass, path):
        # Returns a character subclass of the type passed in.
        # Note: Hi future self. Yes, this probably broke at some point. I don't
        #       know what could be a good fix though, sorry about that.
        #       Hopefully you know more than I do!
        with open(path, 'r') as f:
            character = json.loads(f.read())
        return subclass(**character)
