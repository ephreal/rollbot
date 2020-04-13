# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""


# A mock guild object for testing
class MockGuild():
    def __init__(self, name=None, text_channels=None, users=None):
        self.name = name
        self.text_channels = text_channels
        self.users = users
