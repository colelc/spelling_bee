import os
from src.logging.app_logger import AppLogger
from src.api.request_utils import RequestUtils
from src.service.file_service import FileService

class Scraper(object):
    def __init__(self, config):
        self.logger = AppLogger.get_logger()
        self.spelling_bee_url = config.get("spelling.bee.url")
        self.scrape_file_path = os.path.join(config.get("output.data.dir"), config.get("scrape.file"))
        self.letter_file_path = os.path.join(config.get("output.data.dir"), config.get("letter.file"))
        self.pair_file_path = os.path.join(config.get("output.data.dir"), config.get("pair.file"))

    def scrape(self):
        soup = RequestUtils(self.spelling_bee_url, False).get_data()

        # write out the complete scrape
        FileService.write_file(self.scrape_file_path, soup)

        # letters
        chalkboard_div = soup.select_one("div.spelling-bee-chalkboard")
        FileService.write_file(self.letter_file_path, chalkboard_div)

        letters = chalkboard_div.find_all(class_="chalkboard-letter")
        letter_list = [letter.get_text().upper() for letter in letters]

        # center letter (middle)
        middle_dom = chalkboard_div.find(class_="center-letter")
        middle = middle_dom.get_text().upper()

        # pair list
        pair_container_divs = soup.select('div.pair.letter-label')
        pair_list = [pair_div.get_text().upper() for pair_div in pair_container_divs]
        FileService.write_file(self.pair_file_path, pair_container_divs)

        return {
            "letters" : letter_list,
            "middle": middle,
            "pairs": pair_list
        }
    
