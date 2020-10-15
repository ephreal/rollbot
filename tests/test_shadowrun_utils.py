# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

import asyncio
import unittest
from utils import shadowrun_utils


class TestShadowrunUtils(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_quote(self):
        """
        Ensures that get_quote is able to get a quote and return it properly
        """

        quote = run(shadowrun_utils.get_quote())
        self.assertTrue(isinstance(quote, dict))

    def test_remove_bbcode(self):
        """
        Verifies that the bbcode is stripped from the content properly
        """

        quote = run(shadowrun_utils.get_quote(105))
        quote = run(shadowrun_utils.remove_bbcode(quote))
        self.assertTrue("[b]" not in quote['quote'])
        self.assertTrue("[/b]" not in quote['quote'])

    def test_replace_bbcode(self):
        """
        Verifies that the bbcode is replaced in the content properly
        """

        quote = run(shadowrun_utils.get_quote(105))
        quote = run(shadowrun_utils.remove_bbcode(quote))
        quote = run(shadowrun_utils.replace_bbcode(quote))
        self.assertTrue("[*]" not in quote['quote'])

    def test_format_quote(self):
        """
        Verifies the quote is properly formatted to return to the text channel
        """

        quote = run(shadowrun_utils.get_quote(105))
        quote = run(shadowrun_utils.remove_bbcode(quote))
        quote = run(shadowrun_utils.replace_bbcode(quote))
        quote = run(shadowrun_utils.format_quote(quote))

        self.assertEqual(quote.title, "#105: An artistic scene")


def run(coroutine):
    """
    Runs and returns the data from the couroutine passed in. This is to
    only be used in unittesting.

    coroutine : asyncio coroutine

        -> coroutine return
    """

    return asyncio.get_event_loop().run_until_complete(coroutine)
