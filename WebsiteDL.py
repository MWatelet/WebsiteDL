from os import path
from Accessor import HtmlDownloader, HtmlParser
from pathlib import Path


class WebsiteDL:

    def __init__(self):
        self.table = {}
        dir_path = path.dirname(path.realpath(__file__)) + "/html_files"
        self.downloader = HtmlDownloader(dir_path)
        self.parser = HtmlParser()
        Path(dir_path).mkdir(parents=True, exist_ok=True)

    def run(self, url):
        self.table[url] = []
        file_name = self.downloader.download_html(url)
        references = self.parser.parse_html(file_name)
        references = list(map(lambda x: url if x == "#page" else x, references))
        references = list(filter(lambda x: x != "#", references))
        for referenced_url in references:
            self.update_table(url, referenced_url)
            if referenced_url not in self.table.keys():
                self.run(referenced_url)

    def update_table(self, url, referenced_url):
        if referenced_url not in self.table[url]:
            self.table[url].append(referenced_url)
