# -*- coding: utf-8 -*-

"""
Copyright 2018-2019 Ephreal

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""


import asyncio
import unittest
from classes.dice_rolling import shadowrun_rolling as sr


class TestShadowrun1ERolling(unittest.TestCase):

    def setUp(self):
        self.sr1_roller = sr.Shadowrun1Roller()

    def __run(self, coroutine):
        """
        Runs and returns the data from the couroutine passed in. This is to
        only be used in unittesting.

        coroutine : asyncio coroutine

            -> coroutine return
        """

        return asyncio.get_event_loop().run_until_complete(coroutine)

    def test_roll(self):
        """
        Verifies that the roll function returns a list of integers with numbers
        added up correctly.
        """

        rolls = self.sr1_roller.roll(10)
        rolls = self.__run(rolls)

        self.assertEqual(len(rolls), 10)
        self.assertTrue(6 not in rolls)

    def test_roll_initiative(self):
        """
        Verifies that the initiative roll is returning sane results.
        """

        initiative = self.sr1_roller.roll_initiative(1)
        initiative = self.__run(initiative)
        self.assertTrue(initiative >= 1 and initiative < 8)

    def test_is_failure(self):
        """
        Verifies that the rolls are checked for failures properly.
        """

        rolls = [1, 1, 1, 1, 1]
        failure = self.sr1_roller.is_failure(rolls)
        failure = self.__run(failure)
        self.assertTrue(failure)

        rolls = [1, 1, 1, 1, 2]
        failure = self.sr1_roller.is_failure(rolls)
        failure = self.__run(failure)
        self.assertFalse(failure)

    def test_check_successes(self):
        """
        Tests to verify that successes are being counted properly
        """

        target = 5
        rolls = [6, 5, 4, 3, 2, 1]
        successes = self.sr1_roller.check_successes(target, rolls)
        successes = self.__run(successes)
        self.assertEqual(successes["successes"], 1)
        self.assertEqual(successes["rolls"], [6])

        target = 3
        successes = self.sr1_roller.check_successes(target, rolls)
        successes = self.__run(successes)
        self.assertEqual(successes["successes"], 3)
        self.assertEqual(successes["rolls"], [6, 5, 4])


class TestShadowrun5ERolling(unittest.TestCase):

    def setUp(self):
        self.sr5_roller = sr.Shadowrun5Roller()

    def __run(self, coroutine):
        """
        Runs and returns the data from the couroutine passed in. This is to
        only be used in unittesting.

        coroutine : asyncio coroutine

            -> coroutine return
        """

        return asyncio.get_event_loop().run_until_complete(coroutine)

    def test_roll(self):
        """
        Verifies that the roll function rolls as many dice as expected
        """

        rolls = self.sr5_roller.roll(10)
        rolls = self.__run(rolls)
        self.assertEqual(len(rolls), 10)

        # Tests to make sure that 6's truly explode
        # Put this to 50 dice to make 6's very likely to appear.
        rolls = self.sr5_roller.roll(50, exploding=True)
        rolls = self.__run(rolls)
        self.assertTrue(len(rolls) > 50)

    def test_buy_hits(self):
        """
        Verifies that hits are bought in a 1 hit : 4 dice ratio
        """

        bought = self.sr5_roller.buy_hits(8)
        bought = self.__run(bought)
        self.assertEqual(2, bought)

        bought = self.sr5_roller.buy_hits(9)
        bought = self.__run(bought)
        self.assertEqual(2, bought)

    def count_hits(self):
        """
        Tests that hit counting works as expected
        """

        rolls = [1, 2, 3, 4, 4, 5, 5, 6, 6, 6]
        counted_hits = self.sr5_roller.count_hits(rolls)
        counted_hits = self.__run(counted_hits)

        self.assertEqual(5, counted_hits["hits"])
        self.assertEqual(4, counted_hits["misses"])
        self.assertEqual(1, counted_hits["ones"])

        counted_hits = self.sr5_roller.count_hits(rolls, prime=True)
        counted_hits = self.__run(counted_hits)

        self.assertEqual(7, counted_hits["hits"])
        self.assertEqual(2, counted_hits["misses"])
        self.assertEqual(1, counted_hits["ones"])

    def test_extended_test(self):
        """
        Verifies that extended tests run and accurately determine success or
        failure of the test.
        """

        # Test for failure of test
        extended_test = self.sr5_roller.extended_test(1, 4)
        extended_test = self.__run(extended_test)

        self.assertFalse(extended_test["success"])

        # Test for obvious success
        extended_test = self.sr5_roller.extended_test(50, 4)
        extended_test = self.__run(extended_test)

        self.assertTrue(extended_test["success"])
        self.assertTrue(len(extended_test["rolls"]) < 10)

        # Test for failure even as a prime runner
        extended_test = self.sr5_roller.extended_test(1, 4, prime=True)
        extended_test = self.__run(extended_test)

        self.assertFalse(extended_test["success"])

        # Test for obvious success as a prime runner
        extended_test = self.sr5_roller.extended_test(50, 4, prime=True)
        extended_test = self.__run(extended_test)

        self.assertTrue(extended_test["success"])
        self.assertTrue(len(extended_test["rolls"]) < 10)

    def test_roll_initiative(self):
        """
        Verifies that initiative rolling returns sane results.
        """

        # Test what happens if no modifier is given
        initiative = self.sr5_roller.roll_initiative(1)
        initiative = self.__run(initiative)

        self.assertTrue(initiative >= 1 and initiative <= 6)

        # Verify that adding a modifier works properly too
        initiative = self.sr5_roller.roll_initiative(1, 10)
        initiative = self.__run(initiative)

        self.assertTrue(initiative >= 11 and initiative <= 16)

        # Verify that multiple dice don't cause issues
        initiative = self.sr5_roller.roll_initiative(5, 10)
        initiative = self.__run(initiative)

        self.assertTrue(initiative >= 15)

        # Verify that massive amounts of dice don't cause issues
        initiative = self.sr5_roller.roll_initiative(1000, 10)
        initiative = self.__run(initiative)

        self.assertTrue(initiative >= 1010)
