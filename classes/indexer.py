# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

from nltk.corpus import stopwords

import nltk
import os
import json


class Indexer():
    """
    A very simple file index creator. This is
        1. Only concerned with the file name without the extension
        2. Creates an index of words: {title, file_path}
    """

    def __init__(self, index_path="audio"):
        self.index_path = index_path
        self.index_name = "song_index.json"
        self.ignore_files = [self.index_name, "bot_sounds"]
        self.remove_punctuation = ["[", "]", "(", ")", "\"", ";", ":", "?",
                                   "&", "-"]

    def update_index(self):
        """
        Creates or updates the index. Currently, it is not graceful enough to
        update the index and creates a new file every time.
        """

        index = f"{self.index_path}/{self.index_name}"
        tokens = {}

        for root, dirs, files in os.walk(self.index_path, followlinks=True):
            dirs[:] = [d for d in dirs if d not in self.ignore_files]
            files[:] = [f for f in files if f not in self.ignore_files]

            for name in files:
                self.tokenize(name, root, tokens)

        with open(index, 'w') as f:
            f.write(json.dumps(tokens, sort_keys=True, indent=2))

    def tokenize(self, file_name, root, tokens_dict):
        """
        Modifies a dictionary in place to add additional tokens into it

        file_name: string
        tokens_dict: {tokens: values}

            -> None
        """

        file_path = os.path.join(root, file_name)
        file_name, _ = os.path.splitext(file_name)
        for punc in self.remove_punctuation:
            file_name.replace(punc, " ")
        stop_words = set(stopwords.words('english'))
        word_tokens = nltk.tokenize.word_tokenize(file_name)
        tokens = [t.lower() for t in word_tokens if t not in stop_words]

        for token in tokens:
            try:
                # Note: Currently overwrites songs with the same name and
                #       differing file paths.
                tokens_dict[token][file_name] = file_path
            except KeyError:
                tokens_dict[token] = {file_name: file_path}
