from python:3.6
copy docker_bot/ /docker_bot/
run pip install discord.py==0.16.12
workdir /docker_bot
cmd ["python3", "bot.py"]
