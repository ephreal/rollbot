from python:3.7
copy . .
run pip install discord.py==1.3.3 catapi.py==0.4.0 nltk==3.4.5 PyNaCl==1.3.0
run python -m nltk.downloader all
cmd ["python3", "main.py"]
