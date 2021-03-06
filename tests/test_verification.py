# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

from utils import verification
import asyncio
import unittest


class TestNetwork(unittest.TestCase):
    def setUp(self):
        pass

    def test_is_url(self):
        """
        Verifies that is_url adequately discovers a url
        """

        url = "https://shadowrun.needs.management"
        self.assertTrue(run(verification.is_url(url)))

        url = "https:// www.google.com"
        self.assertFalse(run(verification.is_url(url)))

    def test_process_host_commands(self):
        """
        Ensures that only whitelisted commands are allowed to run
        """

        command = ["df", "-h"]
        output = run(verification.process_host_commands(command))
        self.assertTrue("```\nThat command is not available.```" not in output)

        command = ["ls", "-la"]
        output = run(verification.process_host_commands(command))
        self.assertEqual("```\nThat command is not available.```", output)


def run(coroutine):
    """
    Runs and returns the data from the couroutine passed in. This is to
    only be used in unittesting.

    coroutine : asyncio coroutine

        -> coroutine return
    """

    return asyncio.get_event_loop().run_until_complete(coroutine)
