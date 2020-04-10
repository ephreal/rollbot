# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

import re


async def is_url(url):
    if re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+] | [!*\(\), ]'
                  '|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url):
        return True
    return False
