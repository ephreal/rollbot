# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

from classes.indexer import Indexer

import os
import unittest


class TestIndexer(unittest.TestCase):

    def setUp(self):
        self.index = "tests"
        self.indexer = Indexer(index_path=self.index)

    def tearDown(self):
        os.remove(f"{self.index}/{self.indexer.index_name}")

    def test_update_index(self):
        """
        Tests that the update_index creates an index file.
        """

        self.indexer.update_index()
        self.assertTrue(os.path.exists(self.index))
