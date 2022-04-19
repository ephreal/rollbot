# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""
import argparse


class InvalidArgumentsError(Exception):
    """Raise an InvalidArgumentsError instead of exiting the program"""
    pass


class ThreadParser(argparse.ArgumentParser):
    def __init__(self, *args):
        self.add_argument("-c", "--c", "Create Thread")

    def error(self, message):
        pass
