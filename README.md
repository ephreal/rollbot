# rollbot

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/c18a361a7f2f4d209a4b24a2f3eb1f50)](https://app.codacy.com/app/ephreal/rollbot?utm_source=github.com&utm_medium=referral&utm_content=ephreal/rollbot&utm_campaign=Badge_Grade_Dashboard)

This is a general-purpose discord bot with more server management capabilities and random features slowly being incorporated in when I get hit by something that I really want on it. Along with being good for rolling dice, the bot also has some fun features such as posting a random (or specific) XKCD comic, getting shadowrun/DnD quotes from a quotesite, and more. If you'd like to receive updates on a regular basis or receive help with the bot, please [join the discord guild for the bot.](https://discord.gg/cZXeDPX)

It is also be possible to connect my bot to your discord server if you'd like to use the same bot that I do. [Click here and authorize my bot on your server.](https://discordapp.com/api/oauth2/authorize?client_id=286673190288228362&permissions=502398078&scope=bot) I do my best to have it up as much as possible. If you'd like to support me in my endeavors to make the bot more awesome and reliable, please consider [supporting me on Patreon.](https://www.patreon.com/ephreal)

**Requirements to run this bot yourself**
* [python 3.7+](https://www.python.org/downloads/release/python-373)
* [discord.py](https://github.com/Rapptz/discord.py)
* [aiohttp](https://github.com/aio-libs/aiohttp)
* [nltk](https://www.nltk.org/install.html)
* [pynacl](https://pypi.org/project/PyNaCl/)


**Administrative Bot Features**
* Error logging
* Rebooting/stopping the bot (Must be bot owner)
* Renaming the bot (must be the owner of the bot)
* Setting the bot nickname

**Guild and member management**
* Ban users
* Create roles needed for the bot
* Create needed text channels
* Demote users to a lower role
* Kick users
* Move messages from one channel to another
* Promote users to a higher role
* Purge messages from channels

**Fun commands**
* Get quotes
  * Shadowrun/DnD
  * Inspirobot
* Get jokes
  * dad jokes
  * chuck norris jokes
* Play a "guess the number" game
* Play Rock Paper Scissors
* Play music
* Roll dice
  * Arbitrary dice types (ie: 3d10)
  * DnD
  * Shadowrun
  * Vampire the Masquerade
* Set a timer

To view progress of new feature and features planned for the future, check out [the bot feature project board.](https://github.com/ephreal/rollbot/projects/1)

## Setting up the bot

Setting up the bot requires the following.

* Verifying the bot requirements are installed
* Downloading the bot
* Modifying the configuration file
* Running the bot

### Verifying the bot requirements are installed

Note: If you are running the bot through docker, you will instead need to configure docker for your system. Please see [the docker installation docs](https://docs.docker.com/install/) for information on how to do this. Once docker is installed and configured, skip to [modifying the configuration file.](#modifying-the-configuration-file)

Verify that you have the requirements (listed at the top) installed.

If you don't have these, or you don't know if you do, continue on to the next section.

#### How to install python and all requirements

If you are on windows and need to install python, go here: <https://www.python.org/downloads/release/python-373/>
If you are on Linux, install python 3.7 or above from your repository. I don't know what distro you have, so I won't speculate on the commands needed.
If you are on Mac, I'm sorry, but I have no idea how Mac installation works. Going here should probably get you started though: <https://www.python.org/downloads/release/python-373/>

Follow the install instructions and make sure that pip is installed with python.

Once python is installed, install discord with pip. If you're not sure how to run commands, see here: <https://itconnect.uw.edu/learn/workshops/online-tutorials/web-publishing/what-is-a-terminal/>

```bash
pip install -r requirements.txt
```

The command may differ depending on the version of python/pip you have. If the above fails, try some of these.

```bash
python -m pip install -r requirements.txt

# or
python3 -m pip install -r requirements.txt
```

Once the requirements are installed, you must ensure that nltk downloads all things necessary to use it.

```bash
python -m nltk.downloader all
```

If you still can't get discord installed, try googling your error. There's probably something else going on that you'll need to fix.

### Downloading the bot

Now that you have set up python and discord, download the files for the bot. This can be done by going to the top of the page and clicking on the green button that says "Clone or Download" and choosing "Download Zip". Once that is done, unzip the files and move the folder to wherever makes sense for your system.

Alternatively, the repository can be cloned with git if you have it installed.

```bash
git clone https://github.com/ephreal/rollbot
```

### Modifying the configuration file (OPTIONAL)

Running the bot the first time will walk you through all setup. If you ever need to modify something manually, here is how to do that.

Inside of the downloaded folder, you'll see a folder called "config". Inside here, you'll find a file called "config.json". Open this in notepad/notepad++/sublime/vim/etc. Overwrite YOUR\_TOKEN\_HERE with your bot token. This is necessary to have the bot run.

If you would like to limit the bot to only allow rolling in tabletop, bottesting, and rolling channels, set restrict_rolling to "True".

If you do not have a token yet, refer to here: <https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token>

### Running the bot

There are three ways to run the bot, with the bot_setup.py run button, with python commands, or with docker.

#### Running the bot with bot_setup.py

Once your configuration has been saved, click the "Run Bot" button. The setup window will not allow any more use until you turn off the bot from discord with the halt command.

#### Running the bot with python

Either double click the "main.py" file, or navigate to the main folder in a terminal at run bot.py with

```bash
python main.py
```
If everything goes as expected, the bot will start up and connect to your server.

#### Running the bot with Docker

NOTE: I have only ever ran docker on Linux. The instructions here are for Linux. Please see documentation for your oprating system if you are on a Windows or Mac device.

After downloading and setting up the bot configuration, open a terminal window and verify that you have docker installed and running.

Navigate to the main folder and run

<code>
./docker_build_and_run.sh
</code>
