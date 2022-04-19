# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

import unittest
from utils.shadowland import bbsparser


class TestBbsParser(unittest.TestCase):

    def setUp(self):
        self.parser = bbsparser.BbsParser()

    def test_commands(self):
        """
        Ensure that the commands load properly.
        """

        self.assertTrue("thread" in self.parser.commands)
