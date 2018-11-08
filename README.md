# rollbot

REQUIRES python 3.6.X
Currently python 3.7 breaks the default pip install of discord. When this changes, python 3.7 will be good to use. Use python 3.6.x until then.

This rollbot is a redesign of my older, broken roll bot. I am redesigning it to give it some better code consistiency, cleaner separation of modules, and also learning how to host a bot via docker.

Currently supported roll types are:
* basic dice rolling

Expected future roll types are:
* Shadowrun Dice Rolling (initiative, hits, etc)
* DnD dice rolling

Bonus features that I would like to add on at some point
* Message cleanup of a channel
* DnD character creator
* Shadowrun character roll features (roll perception, roll gymnastics, etc)
* Multiple DnD characters saved and usable


## Setting up the bot

If you are setting this bot up with a docker container, goto SETTING UP BOT WITH DOCKER. Otherwise, read on.

### Running bot with python

Verify that you have the following installed:
* python 3.6.x
* discord.py

If you don't have these, or you don't know if you do, continue on to the next section.

#### Installing python and discord.py

If you are on windows and need to install python, go here: https://www.python.org/downloads/release/python-367/
If you are on Linux, install python 3.6 from your repository. I don't know what distro you have, so I won't even speculate on the commands.
If you are on Mac, I'm sorry. I have no idea how Mac's work. Going here should probably work though: https://www.python.org/downloads/release/python-367/

Follow the install instructions and make sure that pip is installed with python.

Once python is installed, install discord with pip. If you're not sure how to run commands, see here: https://itconnect.uw.edu/learn/workshops/online-tutorials/web-publishing/what-is-a-terminal/

<code>
pip install discord
</code>

The command may differ depending on the version of python/pip you have. If the above fails, try some of these.

<code>
python -m pip install discord

python3 -m pip install discord
</code>

If you still can't get discord installed, google your error. There's probably something else going on that you'll need to fix.


#### Downloading and setting up the bot

Now that you have set up python and discord, download the files for the bot. This can be done by going to the top of the page and clicking on the green button that says "Clone or Download" and choosing "Download Zip". Once that is done, unzip the files and move the folder to wherever makes sense for your system. Inside of the config folder, you'll find a file called "config.json". Open this in notepad/notepad++/sublime/vim/etc. Overwrite YOUR\_TOKEN\_HERE with your bot token.

If you do not have a token yet, refer to here: https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token


#### Running the bot with python

Either double click the "bot.py" file, or navigate to the main folder in a terminal at run bot.py with "python bot.py". If everything goes as expected, the bot will start up and connect to your server.


### Running the bot with Docker

NOTE: I have only ever ran docker on Linux. The instructions here are for Linux.

After downloading and setting up the bot, open a terminal window and verify that you have docker installed and running.

Navigate to the main folder and run 

<code>
./docker\_setup
</code>

to build the docker image. Once the image is completed, run 

<code>
docker run --name bot docker\_bot
</code>

to start the bot.
