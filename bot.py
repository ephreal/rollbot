import discord
import json
import os
import sys

from discord.ext import commands



def load_config():
	with open("config/config.json", 'r') as f:
		return json.load(f)


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


@bot.command()
async def reload():
	await load_cogs()
	await boy.say("Reloaded")

bot.run(config["token"])