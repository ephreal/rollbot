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
        self.connection = sqlite3.connect(self.db)
        self.current_version = self.get_version()

    def get_version(self):
        """
        Gets the current version of the SQL database
        """
        cursor = self.connection.cursor()
        sql = "select version from db_versions where db='schema'"
        try:
            cursor.execute(sql)
        except sqlite3.OperationalError:
            return None
        version = cursor.fetchall()[0][0]
        return version

    def prepare_next_migration(self):
        """
        Imports the next needed migration for use. If there are no more
        migrations, self.current_migration will be set to None
        """

        if self.current_version is None:
            self.migration = getattr(migrations, "migration0")
            self.migration = self.migration.Migration(self.db)
            return

        else:
            for migration in migrations.__all__:
                version = int(migration.replace("migration", ""))
                if version == self.current_version + 1:
                    self.migration = getattr(migrations, migration)
                    self.migration = self.migration.Migration(self.db)
                    return

        # then it appears that there is nothing more to do.
        self.current_version = -1
        self.migration = None

    def migrate(self):
        """
        Rolls the database forward by a single migration.
        Migrations are stored in utils/migrations
        """

        # Closing the connection prior to migrating to ensure the connection
        # does not lock up the database when the migration attempts to run.
        self.connection.close()
        self.migration.migrate()
        self.current_version = self.migration.version
        self.connection = sqlite3.connect(self.db)

    def rollback(self):
        """
        Rolls the database back by a single migration
        """
        pass
