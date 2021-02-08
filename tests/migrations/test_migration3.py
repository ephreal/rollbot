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
from utils.db.migrations import migration3


class TestMigration1(unittest.TestCase):
    def setUp(self):
        self.db = "test.db"
        self.migration = migration3.Migration(self.db)
        self.handler = db_migration_handler.DBMigrationHandler(self.db)

        for i in range(0, 3):
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
        cursor.execute("insert into shadowland_bbs (guild) values (12345)")
        cursor.execute("select guild from shadowland_bbs")
        tag = cursor.fetchall()[0][0]
        self.assertEqual(tag, 12345)

        cursor.execute("select version from db_versions where db='schema'")
        version = cursor.fetchall()[0][0]
        self.assertEqual(version, 3)

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
        self.assertEqual(self.migration.get_schema_version(), 2)
        self.assertFalse(self.migration.failed_migration_pending(["shadowland_bbs"]))

    def test_failed_migration(self):
        """Checks to see if the migration is partially upgraded"""
        self.migration.migrate()
        connection, cursor = self.get_connection()
        sql = "drop table shadowland_bbs"
        cursor.execute(sql)
        connection.commit()
        self.assertTrue(self.migration.failed_migration_pending(["shadowland_bbs"]))

        self.migration.migrated = False
        self.migration.migrate()
        cursor.execute("insert into shadowland_bbs (guild) values (12345)")
        connection.commit()
        self.assertFalse(self.migration.failed_migration_pending(["shadowland_bbs"]))
