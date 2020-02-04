# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

import unittest
from classes.utils import structures


class TestQueue(unittest.TestCase):
    def setUp(self):
        self.queue = structures.Queue(maxlen=6)

    def test_add(self):
        """
        Verifies that adding things to the queue works
        """

        self.queue.add("test")
        self.assertEqual("test", self.queue.items[0])

    def test_empty(self):
        """
        Verifies the queue can test whether it's empty or not correctly
        """

        self.assertTrue(self.queue.empty())
        self.queue.add(5)
        self.assertFalse(self.queue.empty())

    def test_full(self):
        """
        Verifies that full checks it's array properly.
        """
        self.assertFalse(self.queue.full())
        for i in range(0, 6):
            self.queue.add(i)

        self.assertTrue(self.queue.full())

    def test_peek(self):
        """
        Verifies that peek shows the first element and does not remove any
        elements from the queue.
        """
        self.queue.add(3)
        self.assertTrue(3, self.queue.peek())
        self.assertTrue(1, len(self.queue.items))

    def test_remove(self):
        """
        Verifies that the queue is able to remove things from it.
        """

        self.queue.add("test")
        item = self.queue.remove()

        self.assertEqual("test", item)
