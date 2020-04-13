# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""


# A mockup of a discord.Channel object for testing
class MockChannel():
    def __init__(self, name, guild):
        self.guild = guild
        self.name = name
