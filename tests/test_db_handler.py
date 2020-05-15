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
from utils.db import db_migration_handler


class TestDBHandler(unittest.TestCase):
    def setUp(self):
        self.db = "test.db"
        self.handler = db_handler.DBHandler(self.db)
        self.migrations = db_migration_handler.DBMigrationHandler(self.db)
        self.migrations.prepare_next_migration()
        while self.migrations.current_version != -1:
            self.migrations.migrate()
            self.migrations.prepare_next_migration()

    def tearDown(self):
        if os.path.exists(self.db):
            os.remove(self.db)

    def test_cmd_update_commands(self):
        """
        Verifies that update_commands is able to
            1) insert into the database when values do not exist
            2) update values in the database when they do exist
        """

        run(self.handler.metrics.update_commands("uptime", 1))
        c = self.handler.metrics.conn.cursor()

        # Also good to know: the ' ' are required here
        z = c.execute("select name, usage from commands where name = 'uptime'")
        z = z.fetchall()[0]
        self.assertEqual(z[0], "uptime")
        self.assertEqual(z[1], 1)

        run(self.handler.metrics.update_commands("uptime", 4))
        z = c.execute("select name, usage from commands where name = 'uptime'")
        z = z.fetchall()[0]
        self.assertEqual(z[0], "uptime")
        self.assertEqual(z[1], 5)

    def test_cmd_get_usage(self):
        """
        Verifies that get_usage:
            1) does not error out if the value does not exist
            2) returns the correct value
        """
        usage = run(self.handler.metrics.get_usage("uptime"))
        self.assertEqual(usage, 0)

        run(self.handler.metrics.update_commands("uptime", 7))
        usage = run(self.handler.metrics.get_usage("uptime"))
        self.assertEqual(usage, 7)

    def test_cmd_get_all_usage(self):
        """
        Verifies that get_all_usage returns everything in the commands table
        """

        # First verify that it returns nothing if the database is empty
        usage = run(self.handler.metrics.get_all_usage())
        self.assertEqual(len(usage), 0)

        # Insert several things into the db
        run(self.handler.metrics.update_commands("uptime", 7))
        run(self.handler.metrics.update_commands("dnd", 120))
        run(self.handler.metrics.update_commands("halt", 2933182))
        run(self.handler.metrics.update_commands("git", 12344))
        run(self.handler.metrics.update_commands("roll", 22222))

        usage = run(self.handler.metrics.get_all_usage())
        self.assertEqual(len(usage), 5)
        self.assertEqual(usage[0][0], 'halt')

    def test_set_greeting_status(self):
        """
        Verifies that the greeting status can be properly added
        """
        # Enable the greeting for guild 111
        run(self.handler.guilds.set_greeting_status(111, 1))
        status = run(self.handler.guilds.get_greeting_status(111))
        self.assertEqual(status, 1)

        # Disable the greeting for guild 111
        run(self.handler.guilds.set_greeting_status(111, 0))
        status = run(self.handler.guilds.get_greeting_status(111))
        self.assertEqual(status, 0)

    def test_set_greeting(self):
        """
        Verifies that the greeting is set properly
        """

        greeting = "Hello world!"
        run(self.handler.guilds.set_greeting(111, greeting))
        greeting = run(self.handler.guilds.get_greeting(111))
        self.assertEqual(greeting, "Hello world!")

    def test_clear_greeting(self):
        """
        Verifies that the greeting can be properly cleared
        """

        greeting = "Delete me"
        run(self.handler.guilds.set_greeting(111, greeting))
        run(self.handler.guilds.clear_greeting(111))
        greeting = run(self.handler.guilds.get_greeting(111))
        self.assertEqual(greeting, None)

    def test_create_fetch_delete_tag(self):
        """
        Ensures that tags can be added to the database, fetched, and deleted
        Put into one method because you kinda gotta use all parts in order to
        test one piece.
        """

        run(self.handler.tags.create_tag(1, "test", "content is here"))
        content = run(self.handler.tags.fetch_tag(1, "test"))
        self.assertEqual(content, "content is here")

        run(self.handler.tags.delete_tag(1, "test"))
        content = run(self.handler.tags.fetch_tag(1, "test"))
        self.assertEqual(content, None)

    def test_get_and_set_roll_handler(self):
        """
        Ensures the config db is able to insert roll types properly
        """

        run(self.handler.guilds.set_roll_handler(1234, "basic"))
        roll_type = run(self.handler.guilds.get_roll_handler(1234))
        self.assertEqual(roll_type, "basic")

        run(self.handler.guilds.set_roll_handler(1234, "sr3"))
        roll_type = run(self.handler.guilds.get_roll_handler(1234))
        self.assertEqual(roll_type, "sr3")

    def test_get_roll_handler_with_no_guild_id(self):
        """
        Ensures that a roll handler is set and returned if the guild_id and
        roll_type does not exist.
        """

        roll_type = run(self.handler.guilds.get_roll_handler(1234))
        self.assertEqual(roll_type, "basic")

    def test_get_roll_handler_with_no_roll_type(self):
        """
        Ensures that a roll_type of basic is returned when the guild_id exists
        and has no associated roll_type
        """

        run(self.handler.guilds.set_greeting_status(111, 1))
        roll_type = run(self.handler.guilds.get_roll_handler(1234))
        self.assertEqual(roll_type, "basic")


def run(coroutine):
    """
    Runs and returns the data from the couroutine passed in. This is to
    only be used in unittesting.

    coroutine : asyncio coroutine

        -> coroutine return
    """

    return asyncio.get_event_loop().run_until_complete(coroutine)
