# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

from classes.searcher import IndexSearch

import unittest


class TestSearcher(unittest.TestCase):
    def setUp(self):
        self.searcher = IndexSearch()

    def test_search(self):
        """
        Verifies the search function is able to run properly.
        """

        self.searcher.search("Lets go")
