# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

# Replace aiohttp with utils/network.py in the future
import aiohttp
import json
from discord import Colour, Embed


async def get_quote(quote_type=None):
    """
    Fetches a quote from https://shadowrun.needs.management

    quote_type: string
        -> quote: json
    """

    url = "https://shadowrun.needs.management/api/quote"

    try:
        if not quote_type or quote_type == "random":
            pass
        elif quote_type == "latest":
            url += "/latest"
        elif int(quote_type):
            url += f"/{quote_type}"
        else:
            pass

    except Exception:
        pass

    finally:

        async with aiohttp.ClientSession(
              connector=aiohttp.TCPConnector(verify_ssl=True)) as session:

            html = await fetch(session, url)
            html = json.loads(html)

    return html


async def remove_bbcode(quote):
    """
    Removes bbcode content from a quote

    quote: json dict
        -> quote: json dict
    """

    bbcode_tags = [
                    "[b]", "[/b]", "[i]", "[/i]",
                    "[u]", "[/u]", "[s]", "[/s]"
                  ]

    for key in list(quote.keys()):
        if key == "id":
            continue
        replaced = quote[key]
        for i in bbcode_tags:
            replaced = replaced.replace(i, "")
        quote[key] = replaced

    return quote


async def replace_bbcode(quote):
    """
    Replaces certain bbcode with the string equivalents

    quote: json dict
        -> quote: json dict
    """

    content = quote['quote']

    # This seems to be buggy: either all "[*]" are replaced by "    *", or
    # all are replaced with the ol.
    if "[ul]" in content:
        content = content.replace("[ul]", "")
        content = content.replace("[/ul]", "")
        content = content.replace("[*]", "    *")

    elif "[ol]" in content:
        count = 1
        content = content.replace("[ol]", "")
        content = content.replace("[/ol]", "")

        amount = content.count("[*]")

        for _ in range(0, amount):
            current = content.find("[*]")
            start = content[0:current]
            end = content[current+3:]
            content = f"{start}{count}) {end}"
            count += 1

    quote['quote'] = content
    return quote


async def replace_html_escapes(quote):
    """
    Replaces html escapes with their string equivalents

    quote: json dict
        -> quote: json dict
    """

    html_escaped = {
                      "&quot;": '"',
                      "&amp;":  "&",
                      "&#34;": '"',
                      "&#39;": "'",
                    }

    for key in list(quote.keys()):
        if key == "id":
            continue
        replaced = quote[key]
        for i in html_escaped.keys():
            replaced = replaced.replace(i, html_escaped[i])
        quote[key] = replaced

    return quote


async def format_quote(quote):
    """
    Formats the quote for final display.

    quote: json string
        -> discord.Embed
    """
    url = f"{quote['url']}"
    content = Embed(title=f"#{quote['id']}: {quote['title']}", url=url)
    content.set_footer(text=f"Author: {quote['author']}")
    content.description = quote['quote']
    content.colour = Colour.lighter_grey()

    return content


async def fetch(session, url):
    async with session.get(url) as html:
        return await html.text()
