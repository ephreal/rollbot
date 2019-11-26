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
from classes.context_handlers import shadowrun_handler


class TestBaseHandler(unittest.TestCase):

    def setUp(self):
        self.sr1_handler = shadowrun_handler.Shadowrun1Handler()

    def __run(self, coroutine):
        """
        Runs and returns the data from the couroutine passed in. This is to
        only be used in unittesting.

        coroutine : asyncio coroutine

            -> coroutine return
        """

        return asyncio.get_event_loop().run_until_complete(coroutine)

    def test_format_initiative(self):
        """
        Verifies the base handler can format initiative with all handlers
        """

        roll = [3, 3, 3]
        initiative = self.__run(self.sr1_handler.format_initiative(roll, 12))
        self.assertTrue(isinstance(initiative, str))

    def test_roll_initiative(self):
        """
        Verifies the base handler is able to roll initiative with all handlers.
        """

        _, initiative = self.__run(self.sr1_handler.roll_initiative(1, 5))
        self.assertTrue(isinstance(initiative, int))


class TestShadowrunHandler(unittest.TestCase):

    def setUp(self):
        self.handler = shadowrun_handler.ShadowrunHandler()

    def __run(self, coroutine):
        """
        Runs and returns the data from the couroutine passed in. This is to
        only be used in unittesting.

        coroutine : asyncio coroutine

            -> coroutine return
        """

        return asyncio.get_event_loop().run_until_complete(coroutine)

    def test_set_edition(self):
        """
        Verifies the handler is able to set the shadowrun edition
        """

        edition = self.handler.set_sr_edition(1)
        edition = self.__run(edition)
        self.assertEqual(1, self.handler.edition)

        edition = self.handler.set_sr_edition(5)
        edition = self.__run(edition)
        self.assertEqual(5, self.handler.edition)

    def test_check_roll(self):
        """
        Verifies that check_roll works differently for each edition
        """

        roll = [1, 2, 3, 4, 5, 6]
        checked = self.handler.check_roll(roll)
        checked = self.__run(checked)

        self.assertEqual(checked['hits'], 2)

        self.__run(self.handler.set_sr_edition(1))

        checked = self.handler.check_roll(roll)
        checked = self.__run(checked)

        self.assertEqual(checked['successes'], 4)

    def test_extended_test(self):
        """
        Verifies the handler is able to call an extended test
        """

        extended_test = self.handler.extended_test(8, 8)
        extended_test = self.__run(extended_test)

        self.assertTrue(isinstance(extended_test, dict))

    def test_format_extended_test(self):
        """
        Verifies that the handler is able to run the formatter for extended
        tests.
        """

        extended_test = self.handler.extended_test(8, 8)
        extended_test = self.__run(extended_test)

        extended_test = self.handler.format_extended_test(extended_test)
        extended_test = self.__run(extended_test)

        self.assertTrue(isinstance(extended_test, str))

    def test_format_roll(self):
        """
        Verifies that format roll returns the correct information for the
        active shadowrun edition
        """

        roll = [1, 2, 3, 4, 5, 6]

        checked_5e = self.handler.check_roll(roll)
        checked_5e = self.__run(checked_5e)
        glitch = self.__run(self.handler.sr5_is_glitch(roll, 2))

        formatted_5e = self.handler.format_roll(roll, checked_5e,
                                                glitch=glitch)
        formatted_5e = self.__run(formatted_5e)

        self.__run(self.handler.set_sr_edition(1))

        checked_1e = self.handler.check_roll(roll)
        checked_1e = self.__run(checked_1e)

        formatted_1e = self.handler.format_roll(roll, checked_1e)
        formatted_1e = self.__run(formatted_1e)

        self.assertFalse(formatted_1e == formatted_5e)

    def test_is_glitch(self):
        """
        Verifies the handler is capable of checking for glitches.
        """

        roll = [1, 1, 1, 5]
        hits = 1

        glitch = self.__run(self.handler.sr5_is_glitch(roll, hits))

        self.assertTrue(glitch['glitch'])
        self.assertEqual('normal', glitch['type'])

    def test_reroll(self):
        """
        Verifies that rerolling is working correctly
        """

        roll = [1, 2, 3, 4, 5, 6]
        checked = self.__run(self.handler.check_roll(roll))
        self.__run(self.handler.add_roll("test", roll, checked))

        reroll = self.__run(self.handler.reroll('test'))
        roll = reroll['reroll']

        self.assertEqual(self.handler.past_rolls['test']['roll'], roll)

    def test_roll_initiative(self):
        """
        Verifies the formatter is able to roll initiative
        """

        initiative = self.handler.roll_initiative(5, 5)
        _, initiative = self.__run(initiative)

        self.assertTrue(initiative >= 10 and initiative <= 35)


class TestShadowrun1Handler(unittest.TestCase):

    def setUp(self):
        self.handler = shadowrun_handler.Shadowrun1Handler()

    def __run(self, coroutine):
        """
        Runs and returns the data from the couroutine passed in. This is to
        only be used in unittesting.

        coroutine : asyncio coroutine

            -> coroutine return
        """

        return asyncio.get_event_loop().run_until_complete(coroutine)

    def test_check_roll(self):
        """
        Verifies the handler can use the check_roll functionality
        """

        roll = [1, 2, 3, 4, 5, 6]
        checked = self.__run(self.handler.check_roll(roll))

        self.assertEqual(checked['successes'], 4)

    def test_format_roll(self):
        """
        Verifies the handler is able to use the formatter to format rolls.
        """

        roll = [1, 2, 3, 4, 5, 6]
        checked = self.__run(self.handler.check_roll(roll))

        non_verbose = self.__run(self.handler.format_roll(roll, checked,
                                 verbose=False))
        verbose = self.__run(self.handler.format_roll(roll, checked,
                             verbose=True))

        self.assertTrue(len(verbose) > len(non_verbose))

    def test_roll(self):
        """
        Verifies the handler is able to roll 1E dice and do so properly.
        """

        roll = self.__run(self.handler.roll(6))
        self.assertEqual(len(roll), 6)
