# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""


# This is a class that mocks the needed attributes of the context object for
# testing purposes
class MockContext():
    def __init__(self, author=None, channel=None, guild=None):
        self.author = author
        self.channel = channel
        self.guild = guild
