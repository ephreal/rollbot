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
from classes.formatters import shadowrun_formatter as sf


class TestShadowrun1Formatter(unittest.TestCase):

    def setUp(self):
        self.roller = sr.Shadowrun1Roller()
        self.formatter = sf.Shadowrun1Formatter()

    def test_format_roll(self):
        """
        Verifies that the rolls are formatted correctly
        """

        # Check the formatting on a successful roll
        rolls = [1, 3, 3, 4, 6, 12]
        checked = self.roller.check_successes(5, rolls)
        checked = run(checked)

        non_verbose = self.formatter.format_roll(rolls, checked)
        non_verbose = run(non_verbose)

        verbose = self.formatter.format_roll(rolls, checked, verbose=True)
        verbose = run(verbose)

        expected_format = f"Test succeeded\n"\
                          f"You rolled {len(rolls)} dice\n"\
                          f"You had {checked['successes']} successes.\n\n"\
                          f"successes: {checked['successes']}\n"\
                          f"failures: 1"

        self.assertEqual(expected_format, non_verbose)
        self.assertTrue(len(expected_format) < len(verbose))

        # Check the formatting on a failed test
        rolls = [1, 1, 1, 1, 1, 1, 1, 1, 1]
        checked = self.roller.check_successes(5, rolls)
        checked = run(checked)

        non_verbose = self.formatter.format_roll(rolls, checked)
        non_verbose = run(non_verbose)

        verbose = self.formatter.format_roll(rolls, checked, verbose=True)
        verbose = run(verbose)

        expected_format = f"TEST FAILED\n"\
                          f"You rolled {len(rolls)} dice\n"\
                          f"You had {checked['successes']} successes.\n\n"\
                          f"successes: {checked['successes']}\n"\
                          f"failures: 9"

        self.assertEqual(expected_format, non_verbose)
        self.assertTrue(len(expected_format) < len(verbose))

    def test_format_initiative(self):
        """
        Verifies the initiave formatting is correct
        """

        rolls = [5, 5, 5, 5]
        initiative = self.formatter.format_initiative(rolls, 26)
        initiative = run(initiative)

        expected_format = f"Your initiative score is 26"

        self.assertEqual(expected_format, initiative)

    def test_format_unchecked_roll(self):
        """
        Verifies that formatting an unchecked roll is possible.
        """

        roll = [1, 2, 3, 4, 5, 6]
        expected_format = f"You rolled {len(roll)} dice\nRoll: {roll}"
        roll = run(self.formatter.format_unchecked_roll(roll))

        self.assertEqual(roll, expected_format)


class TestShadowrun5Formatter(unittest.TestCase):

    def setUp(self):
        self.formatter = sf.Shadowrun5Formatter()
        self.roller = sr.Shadowrun5Roller()

    def test_buy_hits(self):
        """
        Verifies that buy_hits builds the formatted string correctly.
        """

        dice_pool = 3
        bought = self.formatter.format_buy_hits(dice_pool)
        bought = run(bought)
        expected_format = f"You bought {dice_pool} hits."

        self.assertEqual(expected_format, bought)

    def test_format_roll(self):
        """
        Verifies that the shadowrun 5E hits formatter is formatting rolls
        properly.
        """

        rolls = [1, 2, 3, 4, 5, 6]
        counted = {"hits": 2, "misses": 3, "ones": 1}
        glitch = run(self.roller.is_glitch(rolls, counted['hits']))

        formatted_hits = self.formatter.format_roll(rolls, counted,
                                                    glitch=glitch)
        formatted_hits = run(formatted_hits)

        expected_format = "You rolled 6 dice.\n"\
                          "hits   : 2\n"\
                          "misses : 3\n"\
                          "ones   : 1"

        self.assertEqual(expected_format, formatted_hits)

        # Verify that rolls and hit information from shadowrun rollers are
        # correctly formatted for the formatter.
        rolls = self.roller.roll(6)
        rolls = run(rolls)

        counted = self.roller.count_hits(rolls)
        counted = run(counted)

        glitch = run(self.roller.is_glitch(rolls, counted['hits']))

        formatted_hits = self.formatter.format_roll(rolls, counted,
                                                    )
        formatted_hits = run(formatted_hits)

        expected_format = f"You rolled {len(rolls)} dice.\n"\
                          f"hits   : {counted['hits']}\n"\
                          f"misses : {counted['misses']}\n"\
                          f"ones   : {counted['ones']}"

        self.assertEqual(expected_format, formatted_hits)

    def test_format_extended_test(self):
        """
        Verifies the extended test is formatted properly.
        """
        extended = self.roller.extended_test(8, 8)
        extended = run(extended)

        formatted = self.formatter.format_extended_test(extended)
        formatted = run(formatted)

        self.assertTrue(isinstance(formatted, str))

    def test_format_initiative(self):
        """
        Verifies the initiave formatting is correct
        """

        roll = [5, 5, 5, 5]
        initiative = self.formatter.format_initiative(roll, 26)
        initiative = run(initiative)

        expected_format = f"Your initiative score is 26"

        self.assertEqual(expected_format, initiative)


def run(coroutine):
    """
    Runs and returns the data from the couroutine passed in. This is to
    only be used in unittesting.

    coroutine : asyncio coroutine

        -> coroutine return
    """

    return asyncio.get_event_loop().run_until_complete(coroutine)
