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

    def __str__(self):
        return self.name
