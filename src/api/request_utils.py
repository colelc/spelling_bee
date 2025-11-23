import requests
from bs4 import BeautifulSoup
from src.api.api_utils import ApiUtils
from src.logging.app_logger import AppLogger

class RequestUtils(object):

    def __init__(self, url, debug):
        self.url = url
        self.debug = debug
        self.logger = AppLogger.get_logger()

    def get_data(self):
        self.logger.info("Querying " + self.url)
        response = requests.get(self.url)
        ApiUtils.check_for_api_error(response)

        if self.debug is True:
            ApiUtils.debug(response)

        #info = response.json()
        #self.logger.info(str(info))
        #return info

        html_str = response.text

        try:
            soup = BeautifulSoup(html_str, "html.parser")
            #soup = BeautifulSoup(html_str, "html.parser").prettify().encode("utf-8", errors="replace").decode()
            #self.logger.info(str(soup))
        except UnicodeEncodeError as e:
            self.logger.error("Unicode error: " + str(e))
            
        return soup


  