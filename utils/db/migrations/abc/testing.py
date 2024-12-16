# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

from sqlite3 import OperationalError
from utils.db.migrations.abc import abc_migration


class Migration(abc_migration.Migration):
    """Creates the shadowland tables and views"""
    def __init__(self, db="discord.db"):
        super().__init__(db)
        self.version = 4
        self.description = "Adds game functionality to the DB"""
        self.breaks = "All game functionality requires this"

    def migrate(self):
        """Migrates the database to schema version 4. This means creating the
           games table and associated tables
        """

        if not self.requisites():
            raise ValueError

        games = '''CREATE TABLE IF NOT EXISTS games (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    last_input TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    game_name TEXT
                )'''

        players = '''CREATE TABLE IF NOT EXISTS players (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        game_id INTEGER,
                        player_id INTEGER,
                        current_player INTEGER,
                        FOREIGN KEY (game_id) REFERENCES games (id),
                        FOREIGN KEY (player_id) REFERENCES Users (id)
                  )'''

        # Create the users
        users = '''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT,
                        user_id varchar(30)
                )'''
        
        # Due to the unique constraint on the tag, I need to recreate the tags table
        # and recreate it. This constraint was causing a bug that allows anyone to
        # overwrite the tag of someone else.
        backup_tags = '''CREATE TABLE tags_backup(
                         id INTEGER PRIMARY KEY AUTOINCREMENT not null,
                         user_id varchar(30),
                         tag varchar(100),
                         content varchar(2000),
                         FOREIGN KEY (user_id) REFERENCES users(user_id))'''
        
        # Copy the data from the current tags db into the backup table
        populate_tags = 'INSERT INTO tags_backup SELECT id, user_id, tag, content FROM tags'

        # Delete the current tags db
        remove_tags = 'DROP TABLE tags'

        # Make the backup the primary table
        rename_backup_tags = 'ALTER TABLE tags_backup RENAME TO tags'
        
        # Copy unique user ids into the users table
        populate_current_users = '''INSERT OR IGNORE INTO users (user_id)
                                    SELECT DISTINCT user_id
                                    FROM tags;
                                 '''



        cursor = self.connection.cursor()
        # I'm going to update the schema immediately so that I can revert any
        # changes later just in case this fails to apply completely.
        # In fact... I should add in a check_upgrade_status() method to the
        # abc and declare which tables should exist at each level.
        self.upgrade_table_version("schema")
        self.connection.commit()

        # Execute the SQL statements
        cursor.execute(users)
        cursor.execute(players)
        cursor.execute(games)
        cursor.execute(backup_tags)
        cursor.execute(populate_tags)
        cursor.execute(remote_tags)
        cursor.execute(rename_backup_tags)
        cursor.execute(populate_current_users)

        self.upgrade_table_version("players")
        self.upgrade_table_version("games")
        self.upgrade_table_version("users")
        self.upgrade_table_version("tags")
        self.connection.commit()

        # Remove the shadowland tables since I've realized that idea just...
        # doesn't work like I was hoping it might.
        # I might make a thing that browses the shadowlands news site though.
        tables = ["shadowland_post", "shadowland_thread", "shadowland_bbs",
                  "shadowland_user"]
    
        for table in tables:
            try:
                cursor.execute(f"drop table {table}")
            except OperationalError:
                pass

            self.downgrade_table_version(table)

        self.migrated = True

    def revert(self):
        """Removes all shadowland tables and drops the schema level"""

        if not self.revert_requisites():
            raise ValueError

        cursor = self.connection.cursor()

        # First gotta remove the foreign key mapping
        # Note: I'm *not* adding the UNIQUE constraint to the tag since that *is* a bug.
        # I'm not sure what I was thinking at the time when I added the unique constraint,
        # but I'm sure it was well intentioned. Unfortunately, that causes tags of the same
        # name from different users to be overwritten by whoever used it last.
        remove_foreign_key = '''PRAGMA foreign_keys = OFF;
                                CREATE TABLE tags_backup(id INTEGER PRIMARY KEY AUTOINCREMENT not null,
                                                         user_id varchar(30),
                                                         tag varchar(100),
                                                         content varchar(2000));
                                INSERT INTO tags_backup SELECT id, user_id, tag, content FROM tags;
                                DROP TABLE tags;
                                ALTER TABLE tags_backup RENAME TO tags;
                            '''
        tables = ["players", "users", "games"]
        for table in tables:
            try:
                cursor.execute(f"drop table {table}")
            except OperationalError:
                pass
            self.downgrade_table_version(table)
            self.connection.commit()

        self.downgrade_table_version("schema")

        self.migrated = False

    def revert_requisites(self):
        """Verifies that the database is correctly formatted to revert."""
        version = self.get_schema_version()

        if version == 3:
            return True

        return False

    def requisites(self):
        """Verifies the database schema is equal to 1"""

        tables = ["shadowland_bbs", "shadowland_thread", "shadowland_post",
                  "shadowland_user"]

        # Ensure that a migration did not fail midway.
        if self.failed_migration_pending(tables):
            self.revert()

        if self.get_schema_version() == 2:
            return True
