from urllib.request import urlopen
from urllib.parse import urlparse
import shutil
from bs4 import BeautifulSoup


class HtmlDownloader:

    def __init__(self, dir_path):
        self.dir_path = dir_path

    def download_html(self, url):
        file_name = self.dir_path + "/page_" + urlparse(url).path + ".html"
        with urlopen(url) as response, open(file_name, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
        return file_name


class HtmlParser:

    @staticmethod
    def parse_html(file_name):
        with open(file_name, 'r') as html:
            contents = html.read()
            soup = BeautifulSoup(contents)
            res = [a['href'] for a in soup.find_all('a', href=True)]
            return res
