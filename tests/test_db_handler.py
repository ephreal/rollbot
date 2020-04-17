# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

import asyncio
import os
import unittest
from utils.handlers import db_handler


class TestDBHandler(unittest.TestCase):
    def setUp(self):
        self.db = "test.db"
        self.handler = db_handler.MetricsDB(self.db)
        self.handler.init_tables()

    def tearDown(self):
        if os.path.exists(self.db):
            os.remove(self.db)

    def test_init_tables(self):
        """
        Verifies that the tables:
            1) can be initialized properly.
            2) won't throw errors if initialized multiple times
        """

        self.handler.init_tables()
        c = self.handler.conn.cursor()
        values = c.execute('''select * from commands''')
        values = values.fetchall()
        self.assertEqual(values, [])

    def test_update_commands(self):
        """
        Verifies that update_commands is able to
            1) insert into the database when values do not exist
            2) update values in the database when they do exist
        """

        run(self.handler.update_commands("uptime", 1))
        c = self.handler.conn.cursor()

        # Also good to know: the ' ' are required here
        z = c.execute("select name, usage from commands where name = 'uptime'")
        z = z.fetchall()[0]
        self.assertEqual(z[0], "uptime")
        self.assertEqual(z[1], 1)

        run(self.handler.update_commands("uptime", 4))
        z = c.execute("select name, usage from commands where name = 'uptime'")
        z = z.fetchall()[0]
        self.assertEqual(z[0], "uptime")
        self.assertEqual(z[1], 5)

    def test_get_usage(self):
        """
        Verifies that get_usage:
            1) does not error out if the value does not exist
            2) returns the correct value
        """
        usage = run(self.handler.get_usage("uptime"))
        self.assertEqual(usage, 0)

        run(self.handler.update_commands("uptime", 7))
        usage = run(self.handler.get_usage("uptime"))
        self.assertEqual(usage, 7)

    def test_get_all_usage(self):
        """
        Verifies that get_all_usage returns everything in the commands table
        """

        # First verify that it returns nothing if the database is empty
        usage = run(self.handler.get_all_usage())
        self.assertEqual(len(usage), 0)

        # Insert several things into the db
        run(self.handler.update_commands("uptime", 7))
        run(self.handler.update_commands("dnd", 120))
        run(self.handler.update_commands("halt", 2933182))
        run(self.handler.update_commands("git", 12344))
        run(self.handler.update_commands("roll", 22222))

        usage = run(self.handler.get_all_usage())
        self.assertEqual(len(usage), 5)
        self.assertEqual(usage[0][0], 'halt')


def run(coroutine):
    """
    Runs and returns the data from the couroutine passed in. This is to
    only be used in unittesting.

    coroutine : asyncio coroutine

        -> coroutine return
    """

    return asyncio.get_event_loop().run_until_complete(coroutine)
