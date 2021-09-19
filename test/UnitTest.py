import unittest
from src.WebsiteDL import WebsiteDL


class WebsiteDLTest(unittest.TestCase):

    def sanitize_url_test(self):
        url = "https://coopiteasy.be/"

        web_scrapper = WebsiteDL(url)

        url = "https://coopiteasy.be/main/media/index.html"
        web_scrapper.sanitize_url(url)