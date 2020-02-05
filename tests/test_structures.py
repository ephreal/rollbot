# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

import asyncio
import unittest
from utils import structures


class TestQueue(unittest.TestCase):
    def setUp(self):
        self.queue = structures.Queue(maxlen=6)

    def test_add(self):
        """
        Verifies that adding things to the queue works
        """

        run(self.queue.add("test"))
        self.assertEqual("test", self.queue.items[0])

    def test_empty(self):
        """
        Verifies the queue can test whether it's empty or not correctly
        """

        self.assertTrue(run(self.queue.empty()))
        run(self.queue.add(5))
        self.assertFalse(run(self.queue.empty()))

    def test_full(self):
        """
        Verifies that full checks it's array properly.
        """
        self.assertFalse(run(self.queue.full()))
        for i in range(0, 6):
            run(self.queue.add(i))

        self.assertTrue(run(self.queue.full()))

    def test_peek(self):
        """
        Verifies that peek shows the first element and does not remove any
        elements from the queue.
        """
        run(self.queue.add(3))
        self.assertTrue(3, run(self.queue.peek()))
        self.assertTrue(1, len(self.queue.items))

    def test_remove(self):
        """
        Verifies that the queue is able to remove things from it.
        """

        run(self.queue.add("test"))
        item = run(self.queue.remove())

        self.assertEqual("test", item)


def run(coroutine):
    """
    Runs and returns the data from the couroutine passed in. This is to
    only be used in unittesting.

    coroutine : asyncio coroutine

        -> coroutine return
    """

    return asyncio.get_event_loop().run_until_complete(coroutine)
