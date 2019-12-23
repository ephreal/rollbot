# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""


class Card():
    """
    Basic card class to allow for easier tallying of card totals.

    Class Variables:

        name (str):
            The name of the card when displaying to a player.

        description (str):
            An extended description if more description is needed. For example,
            an uno reverse card might give a brief description of what it does.

        worth
            An int indicating how much the card is worth. Not necessary if it
            doesn't makes sense.

    """

    def __init__(self, name, description=None, worth=None):
        self.name = name
        self.description = description
        # These cards have no self.worth by default. How's it feel card, gonna
        # cry? Whoah, calm down. Let's work on your self.esteem first.....
        self.worth = worth

    def __int__(self):
        if self.worth:
            return self.worth
        return 0

    def __str__(self):
        return self.name
