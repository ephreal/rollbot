# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

import sqlite3
import os
import unittest
from utils.db import db_migration_handler


class TestDBMigrationHandler(unittest.TestCase):
    def setUp(self):
        self.db = "test.db"
        self.handler = db_migration_handler.DBMigrationHandler(self.db)

    def tearDown(self):
        os.remove(self.db)

    def test_prepare_next_migration(self):
        """Verifies that prepare migration gets the correct migration"""
        self.handler.prepare_next_migration()
        self.assertTrue(self.handler.migration)

    def test_migrate(self):
        """Verifies that the database handler is capable of updating"""
        connection = sqlite3.connect(self.db)
        cursor = connection.cursor()
        self.handler.prepare_next_migration()
        self.handler.migrate()
        self.assertEqual(self.handler.current_version, 0)

        cursor.execute("insert into greetings (guild_id,message) values (1,2)")

    def test_migrate_all(self):
        """Verifies an invalid current_version is set when rolling forwards is
           completed"""
        self.handler.migrate_all()
        self.assertEqual(self.handler.current_version, -1)

    def test_rollback(self):
        """Ensures the database can be rolled back safely"""
        self.handler.migrate_all()
        version = self.handler.current_version
        self.handler.connection.close()
        self.handler = db_migration_handler.DBMigrationHandler(self.db)

        self.assertEqual(version, -1)
        self.handler.prepare_previous_migration()
        version = self.handler.current_version

        self.handler.rollback()
        self.assertNotEqual(self.handler.current_version, version)
        self.assertFalse(self.handler.migration.revert_requisites())
        self.assertFalse(self.handler.migration.migrated)
