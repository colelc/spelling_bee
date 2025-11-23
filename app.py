
import json
import itertools
from itertools import groupby
import sys
import time
import urllib.request
from collections import Counter

class App(object):

    @classmethod
    def go(cls):
        ###########################
        #word = "LIJJET"
        #App.consecutive_duplicates(word)
        #sys.exit(0)
        #############################

        endpoint = "https://api.dictionaryapi.dev/api/v2/entries/en/"  #football

        answers = list()

        #N = 4 #  example: value 4 means it's 6-letter word we are looking for (we know the 1st 2 letters)
        N = 2
        known_two = "PI"
        middle = "L"
        letters = list({"L", "T", "M", "E", "I", "N", "P"})

        total_combos = 0
        count = 0
        middle_filter_count = 0
        consecutive_consonants = 0
        consecutive_identical_consonants = 0
        consecutive_identical_vowels = 0
        consecutive_dupes = 0
        customized = 0

        for combo in itertools.product(letters,  repeat=N):
            total_combos += 1

        print("TOTAL combos: " + str(total_combos))

        for combo in itertools.product(letters,  repeat=N):
            count += 1
            if count % 1000 == 0:
                App.totals_update(count, total_combos, middle_filter_count, consecutive_consonants, consecutive_identical_consonants,  consecutive_dupes, customized)

            part = "".join(combo)
            word = known_two +  part

            if not word.__contains__(middle):
                middle_filter_count += 1
                continue

            if App.find_consecutive_consonants(word):
                consecutive_consonants += 1
                continue

            if App.has_consecutive_identical_consonants(word):
                consecutive_identical_consonants += 1
                continue

            if App.has_consecutive_identical_vowels(word):
                consecutive_identical_vowels += 1
                continue


            if App.consecutive_duplicates(word):
                consecutive_dupes += 1
                continue

            if App.customized_daily_checks(word, customized):
                customized += 1
                continue

            print("API call: " + word)

            url = endpoint + word.lower()
            #url = endpoint + "football"
            headers = {"Accept": "application/json", "User-Agent": "Mozilla/5.0"}

            req = urllib.request.Request(url, headers=headers,  method="GET")

            try:
                with urllib.request.urlopen(req) as response:
                    json_string = response.read().decode("UTF-8")
                    payload = json.loads(json_string) #dict
                    print(str(payload))
                    answers.append(word)
            except Exception as e:
                x = None
                #print(str(e))
                #if e.code == 404:
                    #print("word not found: " + word.lower())



            time.sleep(1)

        answers.sort()
        print(str(answers))

    @classmethod
    def totals_update(cls, count:int, total_combos:int,  middle_filter_count:int, consecutive_consonants:int, consecutive_identical_consonants:int, consecutive_identical_vowels:int, consecutive_dupes:int, customized:int) -> None:
        #balance = count - (middle_filter_count + repeat_y_count + repeating_consonant + custom_rule_count)

        pct = (count / total_combos) * 100
        rounded = round(pct, 2)
        print(\
            str(count) + " of " + str(total_combos) + " (" + str(rounded) + "%)" + ": " \
            + str(middle_filter_count) + " no middle, " \
            + str(consecutive_consonants) + " consecutive consonants, " \
            + str(consecutive_identical_consonants) + " consecutive identical consonants, " \
            + str(consecutive_identical_vowels) + " consecutive identical vowels, " \
            + str(consecutive_dupes) + " consecutive dupes, "\
            + str(customized) + " customized " \
            )
                
    @classmethod
    def find_consecutive_consonants(cls, word:str):
        # max number of non-end consecutive consonants is typically 6
        # max number of end consecutive consonants is typically 5
        vowels = set('aeiouAEIOU')
        consecutive_consonants = list()
        n = len(word)
        #print(word)

        # end of word
        if n >= 5:
            for i in range(n - 5):
                if (
                    word[i] not in vowels
                    and word[i+1] not in vowels
                    and word[i+2] not in vowels
                    and word[i+3] not in vowels
                    and word[i+4] not in vowels
                    and word[i+5] not in vowels
                ):
                    consecutive_consonants.append(word[i])
                    if len(consecutive_consonants) > 5:
                        print (word + " -> 5 or more consonants at end of word")
                        return True
                    
        if n >= 6:
            consecutive_consonants = list()
            if (
                word[0] not in vowels
                and word[1] not in vowels
                and word[2] not in vowels
                and word[3] not in vowels
                and word[4] not in vowels
                and word[5] not in vowels
            ):
                consecutive_consonants.append(word[i])
                if len(consecutive_consonants) > 5:
                    print (word + " -> 6 or more consonants at beginning of word")
                    return True               
                
        return False
    
    @classmethod
    def has_consecutive_identical_consonants(cls, word:str, n=3) -> bool:
        vowels = set('AEIOUaeiou')
        prev_char = ''
        count = 0

        for char in word:
            if char.isalpha() and char not in vowels:
                if char == prev_char:
                    count += 1
                else:
                    count = 1
                    prev_char = char
                if count >= n:
                    #print (word + " -> has 3 or more consecutive identical consonants")
                    return True
            else:
                count = 0
                prev_char = ''

        return False
    
    @classmethod
    def has_consecutive_identical_vowels(cls, word:str, n=3) -> bool:
        consonants = set('BCDFGHJKLMNPQRSTVWXYZbcdfghjklmnpqrstvwxyz')
        prev_char = ''
        count = 0

        for char in word:
            if char.isalpha() and char not in consonants:
                if char == prev_char:
                    count += 1
                else:
                    count = 1
                    prev_char = char
                if count >= n:
                    print (word + " -> has 3 or more consecutive identical vowels")
                    return True
            else:
                count = 0
                prev_char = ''

        return False
            
    @classmethod
    def consecutive_duplicates(cls, word:str) -> bool:
        # these consonants are never consecutive
        never = ["H", "J", "V", "X", "Y"]
        # Collect all character groups with length >= 2
        consecutive = [(char, sum(1 for _ in group)) for char, group in groupby(word)]
        #print(word + " -> " + str(consecutive))
        # NEADVGVJJE -> [('N', 1), ('E', 1), ('A', 1), ('D', 1), ('V', 1), ('G', 1), ('V', 1), ('J', 2), ('E', 1)]

        filtered = [tup for tup in consecutive if tup[0] in never and tup[1] == 2]
        #print(str(filtered))

        if filtered:
            #print (word + " -> consecutive restricted consonant" )
            return True
        
        return False
    
    @classmethod
    def customized_daily_checks(cls, word:str, customized: int) -> bool:
        n = len(word)
        vowels = set('aeiouAEIOU')

        if n == 8:
            num_vowels = sum(1 for ch in word if ch in vowels)
            if num_vowels < 3:
                customized += 1
                #print (word + " -> less than 3 vowels in 8-letter word")
                return True

        # if (
        #     word.endswith("TD")
        #     or word.endswith("GD")
        #     or word.endswith("V")
        # ):
        #     customized += 1
        #     #print (word + " customized skip for word ending")
        #     return True

        #if n >= 4:
        # if (
        #     word.startswith("LII") 
        #     or word.startswith("LILN")
        #     ):
        #     customized += 1
        #     print (word + " -> customized skip for word beginning")
        #     return True
            
        return False

App.go()