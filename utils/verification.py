# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

import re
from subprocess import Popen, PIPE


async def is_url(url):
    if re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+] | [!*\(\), ]'
                  '|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url):
        return True
    return False


async def process_host_commands(command):
    """
    Checks the commands against a whitelist before allowing them to run.
    This is to allow only specific commands to run without allowing other
    commands that may cause problems/give up sensitive information to run.

    command: list[str]
        -> command_output (str)
    """

    whitelist = ["uptime", "free", "df"]

    if command[0] in whitelist:

        data = Popen(command, stdout=PIPE)
        data = data.communicate()[0].decode()
        if len(data) > 1950:
            data = data[0:1950]
            data += "\n\n...\nOutput Truncated\n\n"
        return f"```\n{data}```"

    else:
        return "```\nThat command is not available.```"
