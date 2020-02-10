# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""


class Queue:
    # A very simple queue that does not cause blocking when
    # maximum length is reached. Instead of blocking input,
    # it will return None.
    def __init__(self, maxlen=0):
        self.maxlen = maxlen
        self.items = []

    async def add(self, item):
        """
        Add an item to the queue. Returns True if successful, False if not

            -> Boolean
        """
        if not (await self.full()):
            self.items.append(item)
            return True

        return False

    async def clear(self):
        """
        Clears all items from the queue
        """

        self.items = []

    async def is_empty(self):
        """
        Tests whether or not the queue is empty.

        Returns True if is_empty, None if not.
        """

        return len(self.items) == 0

    async def full(self):
        """
        Checks to see if the queue is full. If maxlen is 0, there is assumed
        to be no limit (limited practically by memory size)

        Returns True if full, None if not

            -> True or None
        """

        if (self.maxlen == 0) or (len(self.items) < self.maxlen):
            return None
        return True

    async def peek(self):
        """
        Returns the first item on the queue without removing it.
        """

        if len(self.items) == 0:
            return None
        return self.items[0]

    async def remove(self):
        """
        Removes the first item from the queue. Returns the item to the caller.

            -> first item from queue
        """

        if not (await self.is_empty()):
            item = self.items[0]
            self.items = self.items[1:]
            return item
