# rollbot

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/c18a361a7f2f4d209a4b24a2f3eb1f50)](https://app.codacy.com/app/ephreal/rollbot?utm_source=github.com&utm_medium=referral&utm_content=ephreal/rollbot&utm_campaign=Badge_Grade_Dashboard)

**Requirements**
* [python 3.7+](https://www.python.org/downloads/release/python-373)
* [discord.py](https://github.com/Rapptz/discord.py)
* [aiohttp](https://github.com/aio-libs/aiohttp)

This bot has become a general-purpose discord bot with more server management capabilities slowly being incorporated in. Along with being good for rolling dice, the bot also has some fun features such as posting a random (or specific) XKCD comic, getting shadowrun/DnD quotes from a quotesite, and more.

The bot has been redesigned with better reliability in mind, and it's possible to run the bot in a docker container.

**Bot Features (alphabetized)**
* Get quotes
  * Shadowrun/DnD
  * Inspirobot
* Halt the bot
* Ping the bot
* Play a "guess the number" game
* Play Rock Paper Scissors
* Purge message from a channel
* Reboot the bot
* Reload bot cogs
* Rename the bot
* Roll dice
  * Arbitrary dice types (ie: 3d10)
  * DnD
  * Shadowrun
  * Vampire the Masquerade
* Show guild information
* Spam messages to a channel
* Set a timer

Dice rolling features are still in progress. In particular, Shadowrun has a very complex dice rolling ruleset thta I am still adding new items to. Basic dice rolling is always available when a particular type of dice roll is unavailable.

In addition to the above features, I have recently learned how to automatically update all portions of the bot. I'm looking into how to get automatic updates pushed out for those who would like it.

## Setting up the bot

Setting up the bot requires the following.

* Verifying the bot requirements are installed
* Downloading the bot
* Modifying the configuration file
* Running the bot

### Verifying the bot requirements are installed

Note: If you are running the bot through docker, you will instead need to configure docker for your system. Please see [the docker installation docs](https://docs.docker.com/install/) for information on how to do this. Once docker is installed and configured, skip to [modifying the configuration file.](#modifying-the-configuration-file)

Verify that you have the following installed:
* [python 3.7](https://www.python.org/downloads/release/python-373/)
* [discord.py](https://github.com/Rapptz/discord.py)
* [aiohttp](https://github.com/aio-libs/aiohttp)

If you don't have these, or you don't know if you do, continue on to the next section.

#### How to install python and all requirements

If you are on windows and need to install python, go here: <https://www.python.org/downloads/release/python-373/>
If you are on Linux, install python 3.6 or above from your repository. I don't know what distro you have, so I won't speculate on the commands needed.
If you are on Mac, I'm sorry, but I have no idea how Mac installation works. Going here should probably get you started though: <https://www.python.org/downloads/release/python-373/>

Follow the install instructions and make sure that pip is installed with python.

Once python is installed, install discord with pip. If you're not sure how to run commands, see here: <https://itconnect.uw.edu/learn/workshops/online-tutorials/web-publishing/what-is-a-terminal/>

```bash
pip install discord
pip install aiohttp
```

The command may differ depending on the version of python/pip you have. If the above fails, try some of these.

```bash
python -m pip install discord
python -m pip install aiohttp

# or
python3 -m pip install discord
python3 -m pip install aiohttp
```

If you still can't get discord installed, try googling your error. There's probably something else going on that you'll need to fix.

### Downloading the bot

Now that you have set up python and discord, download the files for the bot. This can be done by going to the top of the page and clicking on the green button that says "Clone or Download" and choosing "Download Zip". Once that is done, unzip the files and move the folder to wherever makes sense for your system.

Alternatively, the repository can be cloned with git if you have it installed.

```bash
git clone https://github.com/ephreal/rollbot
```

### Modifying the configuration file

Once the bot has been downloaded, it's necessary to modify the configuation file and add in your bot token. You can also modify the bot description, bot command prefix, or allowed rolling channels if you desire.

Inside of the downloaded folder, you'll see a folder called "config". Inside here, you'll find a file called "config.json". Open this in notepad/notepad++/sublime/vim/etc. Overwrite YOUR\_TOKEN\_HERE with your bot token. This is necessary to have the bot run.

If you have specific channels you want to limit rolling to, place the name of these channels in the rolling_channels. If you'd like to change the description of the bot, modify description. If you want the bot to use something else as the command prefix ("." by default), then change that too.

If you do not have a token yet, refer to here: <https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token>

### Running the bot

There are two ways to run the bot, with python, or with docker.

#### Running the bot with python

Either double click the "main.py" file, or navigate to the main folder in a terminal at run bot.py with "python main.py". If everything goes as expected, the bot will start up and connect to your server.

#### Running the bot with Docker

NOTE: I have only ever ran docker on Linux. The instructions here are for Linux.

After downloading and setting up the bot configuration, open a terminal window and verify that you have docker installed and running.

Navigate to the main folder and run

<code>
./docker_setup
</code>

to build the docker image. Once the image is completed, run

<code>
sudo docker run --name bot docker_bot
</code>

to start the bot.

To do both steps at once, run

<code>
./docker_setup && sudo docker run --name bot docker_bot
</code>

You can simply run

<code>
sudo docker start bot
</code>

to start the bot if it ever dies after that.
