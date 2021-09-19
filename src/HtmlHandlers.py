from urllib.request import urlopen
from urllib.parse import urlparse
import shutil
from bs4 import BeautifulSoup
from w3lib.url import safe_url_string


class HtmlDownloader:

    def __init__(self, dir_path):
        self.dir_path = dir_path

    def download_html(self, url):
        """
        :param url: url of the html file to download
        :return: name of the local file created with the downloaded html
        """
        file_name = self.dir_path + "/page" + urlparse(url).path.replace("/", "_") + ".html"
        try:
            with urlopen(url) as response, open(file_name, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)
            return file_name
        except UnicodeEncodeError:              # case where we get an iri instead of an uri
            url = safe_url_string(url, encoding="<utf-8>")
            return self.download_html(url)


class HtmlParser:

    @staticmethod
    def parse_html(file_name):
        """
        :param file_name: name of the local html file to parse
        :return: all href links in <a> tags in the file
        """
        with open(file_name, 'r') as html:
            contents = html.read()
            soup = BeautifulSoup(contents, "html.parser")
            hrefs = {a['href'] for a in soup.find_all('a', href=True)}
            return hrefs
