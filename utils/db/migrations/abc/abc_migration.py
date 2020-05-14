# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

from abc import ABC
import sqlite3


class Migration(ABC):
    def __init__(self, db="discord.db"):
        self.connection = sqlite3.connect(db)

    def migrate(self):
        """
        Applies a migration to the database
        """
        pass

    def revert(self):
        """
        Reverts changes done by this migration
        """
        pass

    def requisites(self):
        """
        This must return true for the migration to run.
        """
        pass

    def revert_requisites(self):
        """
        This must return True for the database revert to run
        """
        pass
