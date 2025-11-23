
import json
import itertools
from itertools import groupby
import sys
import time
import urllib.request
from collections import Counter
from config import Config

class App(object):

    @classmethod
    def go(cls):
        answers = list()
        ###########################
        #word = "LIJJET"
        #App.consecutive_duplicates(word)
        #sys.exit(0)
        #############################
        config = Config.set_up_config(".env")

        items = 0
        dictionary = set()
        with open('words_alpha.txt', 'r') as f:
            for line in f:
                items += 1
                #print (line.strip())
                dictionary.add(line.lower().strip())

        print (str(items) + " dictionary items")

        #N = 4 #  example: value 4 means it's 6-letter word we are looking for (we know the 1st 2 letters)
        # = 4
        #known_two = "TO"
        known_two = config.get("known_two")
        #middle = "M"
        middle = config.get("middle")
        #letters = list({"M", "I", "T", "A", "O", "V", "N"})
        letters = [letter.strip() for letter in config.get("letters").split(",")]

        print ("letters: " + str(letters))
        print ("middle: " + middle)
        print ("known_two: " + known_two)

        for N in range(2, 10):
            #total_combos = 0
            #for combo in itertools.product(letters,  repeat=N):
            #    total_combos += 1

            print("")
            #print(str(N) + ": TOTAL combos: " + str(total_combos))

            for combo in itertools.product(letters,  repeat=N):
                part = "".join(combo)
                word = known_two + part

                if not word.__contains__(middle):
                    continue

                #print (word)
                if word.lower().strip() in dictionary:
                    print (str(N+2) + ": " +  word + " is in dictionary")
                    answers.append(word)


        answers.sort()
        print(str(answers))


App.go()