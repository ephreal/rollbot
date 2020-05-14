# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

import sqlite3
from utils.db.migrations.abc import abc_migration


class Migration(abc_migration.Migration):
    """Creates a config table, transfers all data in greetings to config, and
       then drops greetings."""
    def __init__(self, db="discord.db"):
        super().__init__(db)
        self.version = 1

    def requisites(self):
        """
        Verifies that the greetings database is at version 0
        """
        cursor = self.connection.cursor()
        sql = """select version from db_versions where db='greetings'"""
        cursor.execute(sql)
        version = cursor.fetchall()[0][0]
        if version == 0:
            return True
        return False
