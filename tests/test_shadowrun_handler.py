# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""


import asyncio
import unittest
from utils.handlers import shadowrun_handler


class TestBaseHandler(unittest.TestCase):

    def setUp(self):
        self.sr3_handler = shadowrun_handler.Shadowrun3Handler()

    def test_format_initiative(self):
        """
        Verifies the base handler can format initiative with all handlers
        """

        roll = [3, 3, 3]
        initiative = run(self.sr3_handler.format_initiative(roll, 12))
        self.assertTrue(isinstance(initiative, str))

    def test_roll_initiative(self):
        """
        Verifies the base handler is able to roll initiative with all handlers.
        """

        _, initiative = run(self.sr3_handler.roll_initiative(1, 5))
        self.assertTrue(isinstance(initiative, int))


class TestShadowrunHandler(unittest.TestCase):

    def setUp(self):
        self.handler = shadowrun_handler.ShadowrunHandler()

    def test_set_edition(self):
        """
        Verifies the handler is able to set the shadowrun edition
        """

        edition = self.handler.set_sr_edition(3)
        edition = run(edition)
        self.assertEqual(3, self.handler.edition)

        edition = self.handler.set_sr_edition(5)
        edition = run(edition)
        self.assertEqual(5, self.handler.edition)

    def test_check_roll(self):
        """
        Verifies that check_roll works differently for each edition
        """

        roll = [1, 2, 3, 4, 5, 6]
        checked = self.handler.check_roll(roll)
        checked = run(checked)

        self.assertEqual(checked['hits'], 2)

        run(self.handler.set_sr_edition(3))

        checked = self.handler.check_roll(roll)
        checked = run(checked)

        self.assertEqual(checked['successes'], 5)

    def test_extended_test(self):
        """
        Verifies the handler is able to call an extended test
        """

        extended_test = self.handler.extended_test(8, 8)
        extended_test = run(extended_test)

        self.assertTrue(isinstance(extended_test, dict))

    def test_format_extended_test(self):
        """
        Verifies that the handler is able to run the formatter for extended
        tests.
        """

        extended_test = self.handler.extended_test(8, 8)
        extended_test = run(extended_test)

        extended_test = self.handler.format_extended_test(extended_test)
        extended_test = run(extended_test)

        self.assertTrue(isinstance(extended_test, str))

    def test_format_roll(self):
        """
        Verifies that format roll returns the correct information for the
        active shadowrun edition
        """

        roll = [1, 2, 3, 4, 5, 6]

        checked_5e = self.handler.check_roll(roll)
        checked_5e = run(checked_5e)
        glitch = run(self.handler.sr5_is_glitch(roll, 2))

        formatted_5e = self.handler.format_roll(roll, checked_5e,
                                                glitch=glitch)
        formatted_5e = run(formatted_5e)

        run(self.handler.set_sr_edition(3))

        checked_3e = self.handler.check_roll(roll)
        checked_3e = run(checked_3e)

        formatted_3e = self.handler.format_roll(roll, checked_3e)
        formatted_3e = run(formatted_3e)

        self.assertFalse(formatted_3e == formatted_5e)

    def test_is_glitch(self):
        """
        Verifies the handler is capable of checking for glitches.
        """

        roll = [1, 1, 1, 5]
        hits = 1

        glitch = run(self.handler.sr5_is_glitch(roll, hits))

        self.assertTrue(glitch['glitch'])
        self.assertEqual('normal', glitch['type'])

    def test_reroll(self):
        """
        Verifies that rerolling is working correctly
        """

        roll = [1, 2, 3, 4, 5, 6]
        checked = run(self.handler.check_roll(roll))
        run(self.handler.add_roll("test", roll, checked))

        reroll = run(self.handler.reroll('test'))
        roll = reroll['reroll']

        self.assertEqual(self.handler.past_rolls['test']['roll'], roll)


class TestShadowrun3Handler(unittest.TestCase):

    def setUp(self):
        self.handler = shadowrun_handler.Shadowrun3Handler()

    def test_check_roll(self):
        """
        Verifies the handler can use the check_roll functionality
        """

        roll = [1, 2, 3, 4, 5, 6]
        checked = run(self.handler.check_roll(roll))

        self.assertEqual(checked['successes'], 3)

    def test_format_roll(self):
        """
        Verifies the handler is able to use the formatter to format rolls.
        """

        roll = [1, 2, 3, 4, 5, 6]
        checked = run(self.handler.check_roll(roll))

        non_verbose = run(self.handler.format_roll(roll, checked,
                          verbose=False))
        verbose = run(self.handler.format_roll(roll, checked,
                      verbose=True))

        self.assertTrue(len(verbose) > len(non_verbose))

    def test_format_unchecked_roll(self):
        """
        Verifies the handler is able to call format_unchecked_roll without
        issue
        """

        roll = [1, 2, 3, 4, 5, 6]
        expected_format = f"You rolled {len(roll)} dice\nRoll: {roll}"
        roll = run(self.handler.format_unchecked_roll(roll))

        self.assertEqual(roll, expected_format)

    def test_roll(self):
        """
        Verifies the handler is able to roll 3E dice and do so properly.
        """

        roll = run(self.handler.roll(6))
        self.assertEqual(len(roll), 6)


def run(coroutine):
    """
    Runs and returns the data from the couroutine passed in. This is to
    only be used in unittesting.

    coroutine : asyncio coroutine

        -> coroutine return
    """

    return asyncio.get_event_loop().run_until_complete(coroutine)
