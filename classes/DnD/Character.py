# -*- coding: utf-8 -*-

"""
Copyright 2018-2019 Ephreal

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""


class DndCharacter():
    """
    Represents a DnD character.

    Class Attributes
        alignment (str):
            The character's alignment. Ex: Lawful Good
        armor_class (int):
            The character's armor class
        armor (dict):
            A dictionary of all armor the character currently has
        attributes (dict):
            A dictionary of character attribues, their values, and whether the
            character is save proficient in the attribute
        background (str):
            The character's background
        bonds (list):
            A string list of bonds the character has.
        char_class (dict):
            The character's class
        character_description (dict):
            A dictionary containing descriptions of the character as eye color,
            height, and backstory
        character_name (str):
            The character's name
        cur_hp (int):
            The character's current health
        death_saves (dict):
            A dict that contains passed/failed death saves
            {
                "successes" : (int),
                "failures" : (int),
            }
        experience (int):
            The character's current experience points
        features (dict):
            A dictionary list of features that the character has
        flaws (list):
            A string list of flaws the character has
        hit_dice (dict):
            A dict that contains the character's hit dice.
            {"character_class" : {
                "remaining" : (int)(dice remaining),
                "die_type" : (int)(sides on die)
                }
            }
        ideals (list):
            A list of strings that are various ideals the character has
        initiative (int):
            The character's current initiative
        items (dict):
            A dictionary of all items the character has
        max_hp (int):
            The character's maximum health
        money (dict):
            A dict of the copper, silver, electrum, gold and platinum the
            character has.
        personality_traits (list):
            A list of strings that have various personality traits the
            character has
        player_name (str):
            The player this character belongs to
        proficiencies (list):
            A string list of the proficiencies the character has
        proficiency (int):
            The character's proficiency bonus
        race (str):
            The character's race
        skills (dict):
            A dictionary of skills with the required attribute and whether or
            not the character is proficient with that skill
        speed (int):
            The character's speed
        spell_slots (dict):
            A dict of all spells the character knows, how many spell slots are
            remaining, and how many spell slots the character has total
        spellcasting (dict):
            A dict of "caster_class" : "caster_attribute"
        tmp_hp (int):
            Any temporary hitpoints the character has
        weapons (dict):
            A dictionary of any weapons the character has.

    Class Methods

        jsonify_data():
            Returns a dict of all class attributes for easy file writing
    """
    __slots__ = [
                 "alignment", "armor_class", "armor", "attributes",
                 "background", "bonds", "char_class", "character_description",
                 "character_name", "cur_hp", "death_saves", "experience",
                 "features", "flaws", "hit_dice", "ideals", "initiative",
                 "items", "max_hp", "money", "personality_traits",
                 "player_name", "proficiencies", "proficiency", "race",
                 "skills", "speed", "spell_slots", "spellcasting", "tmp_hp",
                 "weapons",
                 "json_keys"
                 ]

    def __init__(self, char_data):

        self.json_keys = char_data.keys()
        self.alignment = char_data["alignment"]
        self.armor_class = char_data["armor_class"]
        self.armor = char_data["armor"]
        self.attributes = char_data["attributes"]
        self.background = char_data["background"]
        self.bonds = char_data["bonds"]
        self.char_class = char_data["char_class"]
        self.character_description = char_data["character_description"]
        self.character_name = char_data["character_name"]
        self.cur_hp = char_data["cur_hp"]
        self.death_saves = char_data["death_saves"]
        self.experience = char_data["experience"]
        self.features = char_data["features"]
        self.flaws = char_data["flaws"]
        self.hit_dice = char_data["hit_dice"]
        self.ideals = char_data["ideals"]
        self.initiative = char_data["initiative"]
        self.items = char_data["items"]
        self.max_hp = char_data["max_hp"]
        self.money = char_data["money"]
        self.personality_traits = char_data["personality_traits"]
        self.player_name = char_data["player_name"]
        self.proficiencies = char_data["proficiencies"]
        self.proficiency = char_data["proficiency"]
        self.race = char_data["race"]
        self.skills = char_data["skills"]
        self.speed = char_data["speed"]
        self.spell_slots = char_data["spell_slots"]
        self.spellcasting = char_data["spellcasting"]
        self.tmp_hp = char_data["tmp_hp"]
        self.weapons = char_data["weapons"]

    def jsonify_data(self):
        """
        Places all class attributes in a single dictionary and returns that
        dictionary.

        returns dict
        """

        class_attributes = {}
        for i in self.json_keys:
            class_attributes[i] = getattr(self, i)

        return class_attributes
