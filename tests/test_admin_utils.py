# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""


import asyncio
import os
import unittest
from tests.mock import mockables
from utils import admin_utils


class TestAdminUtils(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        if os.path.exists("test.log"):
            os.remove("test.log")

    def test_write_shutdown_file(self):
        """Verifies the shutdown message file is created"""
        run(admin_utils.write_shutdown_file())
        self.assertTrue(os.path.exists("poweroff"))
        os.remove("poweroff")

    def test_setup_logging(self):
        """Verifies that logging is adequtely setup"""
        admin_utils.setup_logging(mockables.bot1, "test.log")
        mockables.bot1.logger.log(msg="Hello world!", level=50)
        self.assertTrue(os.path.exists("test.log"))


def run(coroutine):
    """
    Runs and returns the data from the couroutine passed in. This is to
    only be used in unittesting.

    coroutine : asyncio coroutine

        -> coroutine return
    """

    return asyncio.get_event_loop().run_until_complete(coroutine)
