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

    def test_completion_state(self):
        """Verifies an invalid current_version is set when rolling forwards is
           completed"""
        # Note to future self:
        # This presently works, but it will break as soon as you add in another
        # migration. You'll need to create a "migrate_all" method or
        # something to ensure this goes through to completion later.
        for _ in range(2):

            self.handler.prepare_next_migration()
            self.handler.migrate()
        self.handler.prepare_next_migration()
        self.assertEqual(self.handler.current_version, -1)
