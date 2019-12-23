# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

import unittest
from classes.games import card


class TestCardMethods(unittest.TestCase):

    def setUp(self):

        self.card = card.Card(name="test", value=10, description="test card")

    def test_string_method(self):
        """
        Verifies the card returns it's name from the string method.
        """

        name = str(self.card)
        self.assertEqual(self.card.name, name)

    def test_int_method(self):
        """
        Verifies the card returns the value propery from the int methods.
        """

        value = int(self.card)
        self.assertEqual(value, self.card.value)


if __name__ == "__main__":
    unittest.main()
