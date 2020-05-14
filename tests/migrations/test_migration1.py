# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""


import unittest
import os
import sqlite3
from utils.db import db_migration_handler
from utils.db.migrations import migration1


class TestMigration1(unittest.TestCase):
    def setUp(self):
        self.db = "test.db"
        self.migration = migration1.Migration(self.db)
        self.handler = db_migration_handler.DBMigrationHandler(self.db)
        self.handler.prepare_next_migration()
        self.handler.roll_forward()

    def tearDown(self):
        os.remove(self.db)

    def test_requisites(self):
        """Ensures the requisites for running the migration return correct"""
        self.assertTrue(self.migration.requisites())

    def test_migrate(self):
        """Ensures that migration happens without issue"""
        connection = sqlite3.connect(self.db)
        cursor = connection.cursor()
        greeting = """insert into greetings (guild_id,greeting) values
                      (195432110, 'This is such an amazing message.')"""
        cursor.execute(greeting)
        self.migration.migrate()
        cursor.execute("select message from config where guild_id=195432110")
        message = cursor.fetchall()[0][0]
        # Note: The fact that it didn't error out is evidence of the table's
        #       existence
        self.assertEqual(message, "This is such an amazing message.")
        with self.assertRaises(sqlite3.OperationalError):
            cursor.execute("select * from greetings")

    def test_revert_requisites(self):
        """ensures that the reversion requisites are met properly"""
        self.migration.migrate()
        self.assertTrue(self.migration.revert_requisites())

    def test_revert(self):
        """Ensures that reverting the database to the original form works"""
        self.migration.migrate()
        self.migration.revert()
        self.assertFalse(self.migration.revert_requisites())
        with self.assertRaises(ValueError):
            self.migration.revert()
