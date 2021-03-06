# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""


import asyncio
import unittest
from classes.dice_rolling import shadowrun_rolling as sr


class TestShadowrun3ERolling(unittest.TestCase):

    def setUp(self):
        self.sr3_roller = sr.Shadowrun3Roller()

    def test_roll(self):
        """
        Verifies that the roll function returns a list of integers with numbers
        added up correctly.
        """

        rolls = self.sr3_roller.roll(10)
        rolls = run(rolls)

        self.assertEqual(len(rolls), 10)
        self.assertTrue(6 not in rolls)

    def test_roll_initiative(self):
        """
        Verifies that the initiative roll is returning sane results.
        """

        initiative = self.sr3_roller.roll_initiative(1)
        _, initiative = run(initiative)
        self.assertTrue(initiative >= 1 and initiative < 8)

    def test_is_failure(self):
        """
        Verifies that the rolls are checked for failures properly.
        """

        rolls = [1, 1, 1, 1, 1]
        failure = self.sr3_roller.is_failure(rolls)
        failure = run(failure)
        self.assertTrue(failure)

        rolls = [1, 1, 1, 1, 2]
        failure = self.sr3_roller.is_failure(rolls)
        failure = run(failure)
        self.assertFalse(failure)

    def test_check_successes(self):
        """
        Tests to verify that successes are being counted properly
        """

        target = 5
        rolls = [6, 5, 4, 3, 2, 1]
        successes = self.sr3_roller.check_successes(target, rolls)
        successes = run(successes)
        self.assertEqual(successes["successes"], 2)
        self.assertEqual(successes["rolls"], [6, 5])

        target = 3
        successes = self.sr3_roller.check_successes(target, rolls)
        successes = run(successes)
        self.assertEqual(successes["successes"], 4)
        self.assertEqual(successes["rolls"], [6, 5, 4, 3])


class TestShadowrun5ERolling(unittest.TestCase):

    def setUp(self):
        self.sr5_roller = sr.Shadowrun5Roller()

    def test_buy_hits(self):
        """
        Verifies that hits are bought in a 1 hit : 4 dice ratio
        """

        bought = self.sr5_roller.buy_hits(8)
        bought = run(bought)
        self.assertEqual(2, bought)

        bought = self.sr5_roller.buy_hits(9)
        bought = run(bought)
        self.assertEqual(2, bought)

    def count_hits(self):
        """
        Tests that hit counting works as expected
        """

        rolls = [1, 2, 3, 4, 4, 5, 5, 6, 6, 6]
        counted_hits = self.sr5_roller.count_hits(rolls)
        counted_hits = run(counted_hits)

        self.assertEqual(5, counted_hits["hits"])
        self.assertEqual(4, counted_hits["misses"])
        self.assertEqual(1, counted_hits["ones"])

        counted_hits = self.sr5_roller.count_hits(rolls, prime=True)
        counted_hits = run(counted_hits)

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
        extended_test = run(extended_test)

        self.assertFalse(extended_test["success"])

        # Test for obvious success
        extended_test = self.sr5_roller.extended_test(50, 4)
        extended_test = run(extended_test)

        self.assertTrue(extended_test["success"])
        self.assertTrue(len(extended_test["rolls"]) < 10)

        # Test for failure even as a prime runner
        extended_test = self.sr5_roller.extended_test(1, 4, prime=True)
        extended_test = run(extended_test)

        self.assertFalse(extended_test["success"])

        # Test for obvious success as a prime runner
        extended_test = self.sr5_roller.extended_test(50, 4, prime=True)
        extended_test = run(extended_test)

        self.assertTrue(extended_test["success"])
        self.assertTrue(len(extended_test["rolls"]) < 10)

    def test_is_glitch(self):
        """
        Ensures that the glitch counter is counting glitches properly
        """

        # Check for obvious glitch first
        glitch = [1, 1, 1, 5]
        hits = 1

        glitch_check = self.sr5_roller.is_glitch(glitch, hits)
        glitch_check = run(glitch_check)

        self.assertTrue(glitch_check["glitch"])
        self.assertEqual('normal', glitch_check['type'])

        # Check for obvious critical glitch
        glitch = [1, 1, 1, 3]
        hits = 0

        glitch_check = self.sr5_roller.is_glitch(glitch, hits)
        glitch_check = run(glitch_check)

        self.assertTrue(glitch_check["glitch"])
        self.assertEqual('critical', glitch_check['type'])

        # Check for edge case of exactly half dice are ones with some hits
        glitch = [1, 1, 5, 5]
        hits = 2

        glitch_check = self.sr5_roller.is_glitch(glitch, hits)
        glitch_check = run(glitch_check)

        self.assertFalse(glitch_check["glitch"])
        self.assertEqual(None, glitch_check['type'])

        # Verify that this works with roll/ount_hits functions
        # Note, the results are randomize so testing exact values is not
        # possible
        roll = run(self.sr5_roller.roll(6))
        checked = run(self.sr5_roller.count_hits(roll))

        glitch = run(self.sr5_roller.is_glitch(roll, checked["hits"]))

    def test_roll(self):
        """
        Verifies that the roll function rolls as many dice as expected
        """

        rolls = self.sr5_roller.roll(10)
        rolls = run(rolls)
        self.assertEqual(len(rolls), 10)

        # Tests to make sure that 6's truly explode
        # Put this to 50 dice to make 6's very likely to appear.
        rolls = self.sr5_roller.roll(50, exploding=True)
        rolls = run(rolls)
        self.assertTrue(len(rolls) > 50)

    def test_roll_initiative(self):
        """
        Verifies that initiative rolling returns sane results.
        """

        # Test what happens if no modifier is given
        initiative = self.sr5_roller.roll_initiative(1)
        _, initiative = run(initiative)

        self.assertTrue(initiative >= 1 and initiative <= 6)

        # Verify that adding a modifier works properly too
        initiative = self.sr5_roller.roll_initiative(1, 10)
        _, initiative = run(initiative)

        self.assertTrue(initiative >= 11 and initiative <= 16)

        # Verify that multiple dice don't cause issues
        initiative = self.sr5_roller.roll_initiative(5, 10)
        _, initiative = run(initiative)

        self.assertTrue(initiative >= 15)

        # Verify that massive amounts of dice don't cause issues
        initiative = self.sr5_roller.roll_initiative(1000, 10)
        _, initiative = run(initiative)

        self.assertTrue(initiative >= 1010)


def run(coroutine):
    """
    Runs and returns the data from the couroutine passed in. This is to
    only be used in unittesting.

    coroutine : asyncio coroutine

        -> coroutine return
    """

    return asyncio.get_event_loop().run_until_complete(coroutine)
