from python:3.7
copy docker_bot/ /docker_bot/
run pip install discord.py==1.2.3
workdir /docker_bot
cmd ["python3", "bot.py"]
