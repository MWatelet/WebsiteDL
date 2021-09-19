import unittest
from parameterized import parameterized
from src.WebsiteDL import WebsiteDL
from src.HtmlHandlers import HtmlDownloader, HtmlParser


class WebsiteDLTest(unittest.TestCase):

    def setUp(self) -> None:
        url = "https://coopiteasy.be/"
        self.web_scrapper = WebsiteDL(url)

    @parameterized.expand(
        [["https://coopiteasy.be/", "https://coopiteasy.be/"],
         ["https://coopiteasy.be/main/media/index", "https://coopiteasy.be/main/media/index"],
         ["https://coopiteasy.be/main#generator", "https://coopiteasy.be/main#generator"],
         ["https://coopiteasy.be/coolpage.html", "https://coopiteasy.be/coolpage.html"],
         ["/", "https://coopiteasy.be/"],
         ["/main/media/index.html", "https://coopiteasy.be/main/media/index.html"],
         ["#", None],
         ["#page", None]]
    )
    def test_sanitize_url(self, url_to_sanitize, sanitized_url):
        res = self.web_scrapper.sanitize_url(url_to_sanitize)
        assert (res == sanitized_url)

    @parameterized.expand(
        [["https://facebook/coopiteasy/", False],
         ["https://coopiteasy.be/main/supermarche.jpg", False],
         ["https://coopiteasy.be/coolpage.html", False],
         ["https://coopiteasy.be/nos-offres/", True]]
    )
    def test_url_must_be_processed(self, url_to_check, check_result):
        self.web_scrapper.website_urls["https://coopiteasy.be/coolpage.html"] = []
        res = self.web_scrapper.url_must_be_processed(url_to_check)
        assert (res == check_result)


if __name__ == '__main__':
    unittest.main()
