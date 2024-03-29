# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

import os
import sys
import json
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import threading


class SetupBot(ttk.Notebook):
    def __init__(self, master=None):
        self.master = master
        super().__init__(master)

        self.grid()
        self.create_widgets()
        self.place_widgets()

    def create_widgets(self):
        """
        Creates the widgets. Does not handle placement
        """

        with open("config/config.json", "r") as f:
            config = json.loads(f.read())

        self.main_frame = ttk.Frame(self)
        self.sr_config = ttk.Frame(self)

        self.add(self.main_frame, text="Bot Setup")
        self.add(self.sr_config, text="Shadowrun Config")

        self.label_avatar = ttk.Label(self.main_frame, text="Bot avatar")
        self.label_description = ttk.Label(self.main_frame, text="Description")
        self.label_name = ttk.Label(self.main_frame, text="Bot name")
        self.label_prefix = ttk.Label(self.main_frame, text="Bot prefix")
        self.label_token = ttk.Label(self.main_frame, text="Bot token")

        self.bot_avatar = ttk.Entry(self.main_frame, width=60)
        self.bot_description = ttk.Entry(self.main_frame, width=60)
        self.bot_name = ttk.Entry(self.main_frame, width=60)
        self.bot_prefix = ttk.Entry(self.main_frame, width=60)
        self.bot_token = ttk.Entry(self.main_frame, width=60)

        # self.bot_avatar.insert(1, config["avatar"])
        self.bot_description.insert(1, config["description"])
        # self.bot_name.insert(1, config["name"])
        self.bot_prefix.insert(1, config["prefix"])
        self.bot_token.insert(1, config["token"])

        self.button_avatar = ttk.Button(self.main_frame,
                                        text="Select bot image",
                                        command=self.askopenfile)

        self.button_save_config = ttk.Button(self.main_frame,
                                             text="Save Config",
                                             command=self.save_config
                                             )
        self.button_run_bot = ttk.Button(self.main_frame,
                                         text="Run Bot",
                                         command=self.run_bot,
                                         )

        self.label_gmth = ttk.Label(self.sr_config)
        self.label_gmth["text"] = "Glitch when more ones than (dice pool)/2"
        self.label_gfe = ttk.Label(self.sr_config)
        self.label_gfe["text"] = "Normal Glitches fail extended tests"
        self.label_cgfe = ttk.Label(self.sr_config)
        self.label_cgfe["text"] = "Critical Glitches fail extended tests"

        self.gmth = tk.BooleanVar()
        self.gfe = tk.BooleanVar()
        self.cgfe = tk.BooleanVar()

        sr_tweaks = config["sr_tweaks"]

        self.gmth.set(sr_tweaks['glitch_more_than_half'])
        self.gfe.set(sr_tweaks['glitch_fails_extended'])
        self.cgfe.set(sr_tweaks['critical_glitch_fails_extended'])

        self.glitch_more_than_half = ttk.Checkbutton(self.sr_config,
                                                     var=self.gmth)
        self.glitch_fails_extended = ttk.Checkbutton(self.sr_config,
                                                     var=self.gfe)
        self.c_glitch_extended = ttk.Checkbutton(self.sr_config,
                                                 var=self.cgfe)

    def place_widgets(self):
        """
        Places all widgets
        """

        self.label_name.grid(row=0, column=0)
        self.bot_name.grid(row=0, column=1)

        self.label_token.grid(row=1, column=0)
        self.bot_token.grid(row=1, column=1)

        self.label_description.grid(row=2, column=0)
        self.bot_description.grid(row=2, column=1)

        self.label_avatar.grid(row=3, column=0)
        self.bot_avatar.grid(row=3, column=1)
        self.button_avatar.grid(row=3, column=2)

        self.label_prefix.grid(row=4, column=0)
        self.bot_prefix.grid(row=4, column=1)

        self.button_save_config.grid(row=6, column=0)
        self.button_run_bot.grid(row=6, column=1)

        self.label_gmth.grid(row=0, column=0)
        self.glitch_more_than_half.grid(row=0, column=1)

        self.label_gfe.grid(row=1, column=0)
        self.glitch_fails_extended.grid(row=1, column=1)

        self.label_cgfe.grid(row=2, column=0)
        self.c_glitch_extended.grid(row=2, column=1)

    def askopenfile(self):
        filename = filedialog.askopenfile(mode='r')
        if filename:
            self.clear_entry(self.bot_avatar)
            self.bot_avatar.insert(1, filename.name)

    @classmethod
    def clear_entry(self, entry):
        entry.delete(0, tk.END)

    def save_config(self):
        """
        writes the configuration back to the config.json file
        """

        sr_tweaks = {
            "glitch_more_than_half": self.gmth.get(),
            "glitch_fails_extended": self.gfe.get(),
            "critical_glitch_fails_extended": self.cgfe.get()
        }

        config = {
            "token": self.bot_token.get(),
            "name": self.bot_name.get(),
            "description": self.bot_description.get(),
            "avatar": self.bot_avatar.get(),
            "prefix": self.bot_prefix.get(),
            "sr_tweaks": sr_tweaks
        }

        with open("config/config.json", "w") as f:
            f.write(json.dumps(config, indent=4))

    @classmethod
    def run_bot(self):
        """
        Starts the bot with the click of a button.
        """

        print("Starting the bot...")
        th = threading.Thread(target=self.start_bot)
        th.start()

    @classmethod
    def start_bot(self):
        os.system(f"{sys.executable} main.py")


root = tk.Tk()
app = SetupBot(root)
app.mainloop()
