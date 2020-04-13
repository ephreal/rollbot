# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""


from tests.mock.MockChannel import MockChannel
from tests.mock.MockContext import MockContext
from tests.mock.MockGuild import MockGuild
from tests.mock.MockUser import MockUser
# This module implements all the classes in the mock directory. This is to
# make testing the modules easier.

guild1 = MockGuild("guild1")
guild2 = MockGuild("guild2")
guild3 = MockGuild("guild3")

text_channels1 = ["rolling", "bottesting", "general", "chill-chat"]
text_channels2 = ["lounge", "chill", "rolling", "testing", "nsfw"]
text_channels3 = ["general", "conspiracy", "name-hidden"]

users1 = ["tom", "sho", "lo", "alli", "zorp", "blamflam", "kidtun"]
users2 = ["sid", "cecil", "rydia", "kain"]
users3 = ["nicole", "jason", "fred", "tom", "grimreaper"]

guild1.text_channels = [MockChannel(chan, guild1) for chan in text_channels1]
guild2.text_channels = [MockChannel(chan, guild2) for chan in text_channels2]
guild3.text_channels = [MockChannel(chan, guild3) for chan in text_channels3]

guild1.users = []
guild2.users = []
guild3.users = []

for i in range(0, len(users1)):
    guild1.users.append(MockUser(i, users1[i], guild1))

for i in range(0, len(users2)):
    guild2.users.append(MockUser(i, users2[i], guild2))

for i in range(0, len(users3)):
    guild3.users.append(MockUser(i, users3[i], guild3))

context1 = MockContext(guild1.users[3], guild1.text_channels[2], guild1)
context2 = MockContext(guild2.users[0], guild2.text_channels[2], guild2)
context3 = MockContext(guild3.users[3], guild3.text_channels[1], guild3)
