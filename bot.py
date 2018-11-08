# -*- coding: utf-8 -*-

"""
Copyright 2018 Ephreal

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
DEALINGS IN THE SOFTWARE.
"""


import discord
import json
import os
import sys

from discord.ext import commands



def load_config():
	with open("config/config.json", 'r') as f:
		return json.load(f)

def get_admins():
	with open("config/admin.json", "r") as f:
		return json.load(f)["admins"]


config = load_config()

bot = commands.Bot(command_prefix=config["prefix"],
	               description="rollbot")

@bot.event
async def on_ready():
	print("Startup complete, loading Cogs....")
	await load_cogs()
	print("Cog loading complete.")


async def load_cogs():
	
	modules = [
			   "cogs.admin",
			   "cogs.roller",
			   "cogs.tests"
			  ]
	
	for extension in modules:
		try:
			print(f"Loading {extension}...")
			bot.load_extension(f"{extension}")
			print(f"Loaded {extension.split('.')[-1]}")

		except Exception as e:
			print(f"Failed to load {extension}")
			print("Error follows...\n")
			print(f"{e}\n")


@bot.command(hidden=True)
async def reload():
	await load_cogs()
	await boy.say("Reloaded")

@bot.command(hidden=True, pass_context=True)
async def stop(ctx):
	admins = await get_admins()

	if ctx.message.author.id not in admins:
		return await bot.say("Please don't try turn me off.")

	await bot.say("Shutting do...")
	sys.exit()

bot.run(config["token"])