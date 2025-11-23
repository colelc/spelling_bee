import os
import json
import itertools
from itertools import groupby
import sys
import time
import urllib.request
from collections import Counter
from src.config.config import Config
from src.logging.app_logger import AppLogger

class WordLookup(object):
    def __init__(self, word_config: dict):
        self.logger = AppLogger.get_logger()

        self.word_file_path = word_config.get("word_file_path")
        self.known_two = word_config.get("known_two")
        self.middle = word_config.get("middle")
        self.letters = word_config.get("letters")
        self.max_word_length = word_config.get("max_word_length")


    def search(self):
        answers = list()
        #word_file = config.get("word.file")
        #input_data_dir = config.get("input.data.dir")
        #word_file_path = os.path.join(input_data_dir, word_file)

        items = 0
        dictionary = set()
        with open(self.word_file_path, 'r') as f:
            for line in f:
                items += 1
                #self.logger.info (line.strip())
                dictionary.add(line.lower().strip())

        self.logger.info(str(items) + " dictionary items")

        #N = 4 #  example: value 4 means it's 6-letter word we are looking for (we know the 1st 2 letters)
        # = 4
        #known_two = "TO"
        #known_two = config.get("known_two")
        #middle = "M"
        #middle = config.get("middle")
        #letters = list({"M", "I", "T", "A", "O", "V", "N"})
        #letters = [letter.strip() for letter in config.get("letters").split(",")]

        #max_word_length = int(config.get("max.word.length")) or 9

        self.logger.info ("letters: " + str(self.letters))
        self.logger.info ("middle: " + self.middle)
        self.logger.info ("known_two: " + self.known_two)

        for N in range(2, self.max_word_length):
            #total_combos = 0
            #for combo in itertools.product(letters,  repeat=N):
            #    total_combos += 1

            self.logger.info("")
            #self.logger.info(str(N) + ": TOTAL combos: " + str(total_combos))

            for combo in itertools.product(self.letters,  repeat=N):
                part = "".join(combo)
                word = self.known_two + part

                if not word.__contains__(self.middle):
                    continue

                #self.logger.info (word)
                if word.lower().strip() in dictionary:
                    self.logger.info (str(N+2) + ": " +  word + " is in dictionary")
                    answers.append(word)


        answers.sort()
        self.logger.info(str(answers))


