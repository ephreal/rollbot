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

    def add(self, item):
        """
        Add an item to the queue. Returns True if successful, False if not

            -> Boolean
        """
        if not self.full():
            self.items.append(item)
            return True

        return False

    def empty(self):
        """
        Tests whether or not the queue is empty.

        Returns True if empty, None if not.
        """

        if len(self.items) == 0:
            return True

    def full(self):
        """
        Checks to see if the queue is full. If maxlen is 0, there is assumed
        to be no limit (limited practically by memory size)

        Returns True if full, None if not

            -> True or None
        """

        print(self.maxlen)
        print(len(self.items))
        if (self.maxlen == 0) or (len(self.items) < self.maxlen):
            return None
        return True

    def peek(self):
        """
        Returns the first item on the queue without removing it.
        """

        return self.items[0]

    def remove(self):
        """
        Removes the first item from the queue. Returns the item to the caller.

            -> first item from queue
        """

        if not self.empty():
            item = self.items[0]
            self.items = self.items[1:]
            return item
