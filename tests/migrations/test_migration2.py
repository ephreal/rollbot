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
from utils.db.migrations import migration2


class TestMigration1(unittest.TestCase):
    def setUp(self):
        self.db = "test.db"
        self.migration = migration2.Migration(self.db)
        self.handler = db_migration_handler.DBMigrationHandler(self.db)
        self.handler.prepare_next_migration()
        self.handler.migrate()
        self.handler.prepare_next_migration()
        self.handler.migrate()

    def tearDown(self):
        os.remove(self.db)

    def get_connection(self):
        connection = sqlite3.connect(self.db)
        cursor = connection.cursor()
        return (connection, cursor)

    def test_requisites(self):
        """Ensures the requisites for running the migration return correct"""
        self.assertTrue(self.migration.requisites())

    def test_migrate(self):
        """Ensures that migration happens without issue"""

        self.migration.migrate()
        self.migration.connection.close()
        connection, cursor = self.get_connection()
        cursor.execute("insert into guild_tags (tag) values ('test')")
        cursor.execute("select tag from guild_tags")
        tag = cursor.fetchall()[0][0]
        self.assertEqual(tag, "test")

        cursor.execute("select version from db_versions where db='schema'")
        version = cursor.fetchall()[0][0]
        self.assertEqual(version, 2)

    def test_revert_requisites(self):
        """ensures that the reversion requisites are met properly"""
        self.migration.migrate()
        connection, cursor = self.get_connection()
        self.assertTrue(self.migration.revert_requisites())

    def test_revert(self):
        """Ensures that reverting the database to the original form works"""
        self.migration.migrate()
        self.migration.revert()
        self.assertFalse(self.migration.revert_requisites())
        with self.assertRaises(ValueError):
            self.migration.revert()
