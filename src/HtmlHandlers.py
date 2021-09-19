from urllib.request import urlopen
from urllib.parse import urlparse
import shutil
from bs4 import BeautifulSoup
from w3lib.url import safe_url_string
from os import path


class HtmlDownloader:

    def __init__(self, dir_path):
        self.local_folder_path = dir_path

    def save_page_to_local_file(self, url):
        """
        :param url: url of the html file to download
        :return: name of the local file created with the downloaded html
        """
        file_name = path.join(self.local_folder_path, "page" + urlparse(url).path.replace("/", "_") + ".html")
        try:
            return self.download_html(file_name, url)
        except UnicodeEncodeError:  # case where we get an iri instead of an uri
            url = safe_url_string(url, encoding="<utf-8>")
            return self.download_html(file_name, url)

    @staticmethod
    def download_html(file_name, url):
        """
        download the html file and create the local copy
        :return: the name of the local file
        """
        with urlopen(url) as response, open(file_name, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
        return file_name


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
            urls_set = {a['href'] for a in soup.find_all('a', href=True)}
            return urls_set
