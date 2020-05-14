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
from utils.db.migrations import migration0


class TestMigration1(unittest.TestCase):
    def setUp(self):
        self.db = "test.db"
        self.migration = migration0.Migration(self.db)

    def tearDown(self):
        os.remove(self.db)

    def test_requisites(self):
        """Ensures the requisites for running the migration return correct"""
        self.assertTrue(self.migration.requisites())

    def test_migrate(self):
        """Ensures that migration happens without issue"""
        self.migration.migrate()
        connection = sqlite3.connect(self.db)
        cursor = connection.cursor()
        cursor.execute("select tag from tags")
        tag = cursor.fetchall()
        self.assertEqual(tag, [])

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
