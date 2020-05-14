# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

import sqlite3
from utils.db import migrations


class DBMigrationHandler():
    """
    Handles database updates in a safe manner.

    Rollbacks are not yet supported.
    """

    def __init__(self, db="discord.db"):
        self.db = db
        self.current_version = self.get_version()

    def get_version(self):
        """
        Gets the current version of the SQL database
        """
        connection = sqlite3.connect(self.db)
        cursor = connection.cursor()
        sql = "select version from db_versions where db='schema'"
        try:
            cursor.execute(sql)
        except sqlite3.OperationalError:
            connection.close()
            return None
        connection.close()
        return cursor.fetchall()[0][0]

    def prepare_next_migration(self):
        """
        Imports the next needed migration for use. If there are no more
        migrations, self.current_migration will be set to None
        """

        if self.current_version is None:
            self.migration = getattr(migrations, "migration0")
            self.migration = self.migration.Migration()
            return

        else:
            for migration in migrations.__all__:
                version = int(migration.replace("migration", ""))
                if version == self.current_version + 1:
                    self.migration = getattr(migrations, migration)
                    self.migration = self.migration.Migration()
                    return

        # then it appears that there is nothing more to do.
        self.current_version = -1
        self.migration = None

    def roll_forward(self):
        """
        Rolls the database forward by a single migration.
        Migrations are stored in utils/migrations
        """
        self.migration.migrate()
        self.current_version = self.migration.version

    def roll_back(self):
        """
        Rolls the database back by a single migration
        """
        pass
