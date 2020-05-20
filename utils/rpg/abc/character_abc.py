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

    def roll_attribute(self, attribute, modifier):
        pass

    def roll_skill(self, skill, modifier):
        pass

    def roll_spell(self, spell, modifier):
        pass

    def to_json(self):
        character = {}
        for attribute in self.__slots__:
            character[attribute] = getattr(self, attribute, None)
        return character

    @staticmethod
    def from_json_file(subclass, path):
        # Returns a character subclass of the type passed in.
        # Note: Hi future self. Yes, this probably broke at some point. I don't
        #       know what could be a good fix though, sorry about that.
        #       Hopefully you know more than I do!
        with open(path, 'r') as f:
            character = json.loads(f.read())
        return subclass(**character)
