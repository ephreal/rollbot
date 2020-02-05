# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

from utils import network
import asyncio
import json
import unittest


class TestNetwork(unittest.TestCase):
    def setUp(self):
        pass

    def test_fetch_page(self):
        """
        Verifies that test_page retrieves a page correctly.
        """

        url = 'https://shadowrun.needs.management/api.php?quote_id=5'
        page = run(network.fetch_page(url))
        quote = json.loads(page)
        self.assertEqual(quote['id'], '5')
        self.assertEqual(quote['title'], "Hellhound Happenings")


def run(coroutine):
    """
    Runs and returns the data from the couroutine passed in. This is to
    only be used in unittesting.

    coroutine : asyncio coroutine

        -> coroutine return
    """

    return asyncio.get_event_loop().run_until_complete(coroutine)
