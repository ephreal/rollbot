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

    async def discord_formatting(self):
        """
        Formats a character object for display in discord. This includes:
            character name
            character race
            character sex
            character age
            character karma
            character attributes
            character condition
        """

        message = []
        message.append(f"name: {self.name}")
        message.append(f"race: {self.race}")
        message.append(f"{self.sex}")
        message.append(f"age: {self.age}")
        message.append(f"karma: {self.karma}")
        message.append(f"attributes: {await self.format_attributes()}")
        message.append(f"{await self.format_condition()}")
        return "\n".join(message)

    async def format_attributes(self):
        """
        Formatts all attributes for ease of reading
        """

        attributes = []
        bod = self.attributes['body']
        qui = self.attributes['quickness']
        str = self.attributes['strength']
        wil = self.attributes['willpower']
        itl = self.attributes['intelligence']
        cha = self.attributes['charisma']
        mag = self.attributes['magic']
        ess = self.attributes['essence']
        attributes.append(f"B: {bod['base']}({bod['base'] + bod['modifier']})")
        attributes.append(f"Q: {qui['base']}({qui['base'] + qui['modifier']})")
        attributes.append(f"S: {str['base']}({str['base'] + str['modifier']})")
        attributes.append(f"W: {wil['base']}({wil['base'] + wil['modifier']})")
        attributes.append(f"I: {itl['base']}({itl['base'] + itl['modifier']})")
        attributes.append(f"C: {cha['base']}({cha['base'] + cha['modifier']})")
        attributes.append(f"M: {mag['base']}({mag['base'] + mag['modifier']})")
        attributes.append(f"E: {ess['base']}({ess['base'] + ess['modifier']})")

        return "   ".join(attributes)

    async def format_condition(self):
        """
        Formats the condition monitor of a character for ease of reading
        """

        d_stun = ":orange_circle:"
        d_physical = ":red_circle:"
        d_overflow = ":skull_crossbones:"
        not_hit = ":black_circle:"

        physical = self.condition['physical']
        physical = f"{d_physical * physical}{not_hit * (10 - physical)}" \
                   f"({physical % 11}/10)"
        physical = f"PHYS:{physical}"

        stun = self.condition['stun']
        stun = f"{d_stun * stun}{not_hit * (10 - stun)} ({stun % 11}/10)"
        stun = f"STUN:{stun}"

        overflow = self.condition['overflow']
        body = self.attributes['body']['base']
        overflow = f"{d_overflow * overflow}{not_hit * (body - overflow)}" \
                   f"({overflow % (body+1)}/{body})"
        overflow = f"OVER:{overflow}"

        return "\n".join([stun, physical, overflow])

    async def get_skill(self, skill, category):
        """
        Gets a skill. Throws a KeyError if the attribute does not exist

        category: active, knowledge
        """
        try:
            return self.skills[category][skill]
        except KeyError:
            skill = await self.get_specialization(skill, category)

        return skill

    async def get_specialization(self, specialization, category='active'):
        """
        Checks for a specialization
        """

        spec = None
        skills = self.skills[category]

        for skill in skills:
            if specialization in list(skills[skill]['specializations'].keys()):
                spec = skills[skill]['specializations'][specialization]
                break
        return spec

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

        attribute = await self.get_attribute(attribute)
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
        attribute = await self.get_attribute(attribute)
        attribute['override'] = override
        return attribute

    async def modify_physical_condition(self, modifier):
        """
        Modifier the character's physical condition monitor
        """

        # Remove from overflow first when removing from the physical monitor
        if modifier < 0 and self.condition['overflow']:
            temp = modifier + self.condition['overflow']
            # Check if there was more overflow than modifier
            if temp > 0:
                self.condition['overflow'] += modifier
                return self.condition
            else:
                modifier += self.condition['overflow']
                self.condition['overflow'] = 0

        self.condition['physical'] += modifier
        if self.condition['physical'] > 10:
            self.condition['overflow'] = (self.condition['physical'] - 10)
            self.condition['physical'] -= self.condition['overflow']

        elif self.condition['physical'] < 0:
            self.condition['physical'] = 0

        if self.condition['overflow'] > self.attributes['body']['base']:
            self.condition['overflow'] = self.attributes['body']['base']

        elif self.condition['overflow'] < 0:
            self.condition['overflow'] = 0

        return self.condition

    async def modify_stun_condition(self, modifier):
        """
        Modify the character's stun condition monitor
        """

        self.condition['stun'] += modifier
        if self.condition['stun'] > 10:
            modifier = self.condition['stun'] - 10
            self.condition['stun'] = 10
            await self.modify_physical_condition(modifier)

        elif self.condition['stun'] < 0:
            self.condition['stun'] = 0

        return self.condition
