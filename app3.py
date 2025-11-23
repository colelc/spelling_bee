import os
import itertools
from src.config.config import Config
from src.logging.app_logger import AppLogger
from src.service.word_lookup import WordLookup

class App(object):

    @classmethod
    def go(cls):

        logger = AppLogger.set_up_logger("app.log")
        config = Config.set_up_config(".env")

        word_config = {
            "word_file_path" : os.path.join(config.get("input.data.dir"), config.get("word.file")),
            "known_two": config.get("known_two"),
            "middle": config.get("middle"),
            "letters":  [letter.strip() for letter in config.get("letters").split(",")],
            "max_word_length": int(config.get("max.word.length")) or 9
        }

        WordLookup(word_config).search()




App.go()