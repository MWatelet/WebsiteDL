from urllib.request import urlopen
from urllib.parse import urlparse
from os import path
import shutil
from pathlib import Path


class Downloader:

    def __init__(self):
        self.dir_path = path.dirname(path.realpath(__file__)) + "/html_files"
        Path(self.dir_path).mkdir(parents=True, exist_ok=True)

    def download_html(self, url):
        file_name = self.dir_path + "/page_" + urlparse(url).path + ".html"
        with urlopen(url) as response, open(file_name, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
