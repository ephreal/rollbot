# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""


import aiohttp


async def fetch_page(url):
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        return html


async def fetch(session, url):
    async with session.get(url) as html:
        return await html.text()
