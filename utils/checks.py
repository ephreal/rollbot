# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""


def check_author(author):
    """
    Checks to see if the author of a message is the same as the author
    passed in.
    """

    def check_message(message):
        return message.author == author
    return check_message
