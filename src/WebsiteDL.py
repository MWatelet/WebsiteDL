from os import path
from HtmlHandlers import HtmlDownloader, HtmlParser
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlparse

EXTENSIONS = [".jpg", ".jpeg", ".mp4", ".webm", ".ogg", ".mp3", ".wav", ".png", ".gif"]


class WebsiteDL:

    def __init__(self, url):
        if url[-1] != "/":  # to standardize the url format given by the user
            url = url + "/"
        self.base_url = url
        self.website_urls = {}  # will contain the plan of the website as a m*n table
        domain = urlparse(url).netloc  # name of the site
        folder_path = path.dirname(path.realpath(__file__)) + "/html_files"
        Path(folder_path).mkdir(parents=True, exist_ok=True)  # creation of the local repository for the html files we'll download
        site_folder_path = path.join(folder_path, domain)
        Path(site_folder_path).mkdir(parents=True, exist_ok=True)
        self.downloader = HtmlDownloader(site_folder_path)
        self.parser = HtmlParser()

    def run(self):
        """
        initial call of the recursive_search_process to not pass the base_url twice to this class and for clarity sake
        """
        self.recursive_search_process(self.base_url)

    def recursive_search_process(self, current_url):
        """
        recursive search of all the files and links in the website
        :param current_url: url of the html file to inspect
        """
        self.website_urls[current_url] = []
        try:
            file_name = self.downloader.save_page_to_local_file(current_url)  # attempt to download the html file
        except HTTPError as error:
            print(current_url + " : ", end="")  # error 404, for example, are caught here
            print(error)
            return
        urls_in_page = self.parser.parse_html(file_name)  # find all the links in the html file
        urls_in_page = set(map(self.sanitize_url, urls_in_page))
        urls_in_page.remove(None)

        for referenced_url in urls_in_page:
            self.store(current_url, referenced_url)  # store the fact that this page has a link to this referenced url
            if self.url_must_be_processed(referenced_url):
                self.recursive_search_process(referenced_url)  # recursive call

    def store(self, base_url, target_url):
        """
        add the target_url if needed to the website_urls
        :param base_url: url of the html page with a link to the target_url within
        :param target_url: url of a link contained in the html file of base url
        """
        if target_url not in self.website_urls[base_url]:
            self.website_urls[base_url].append(target_url)

    @staticmethod
    def detect_media(url):
        """
        detect if the url target a media file
        :return: boolean
        """
        path_to_inspect = urlparse(url).path
        ext = path.splitext(path_to_inspect)[1]
        return ext not in EXTENSIONS

    def url_must_be_processed(self, url):
        """
        check if the url is worth exploring
        """
        # condition 1 : url has not been explored yet
        # condition 2 : url is not containing a media (we are looking for html files only)
        # condition 3 : url does not lead to another website (facebook link for example)
        return url not in self.website_urls.keys() \
               and self.detect_media(url) \
               and self.base_url in url

    def sanitize_url(self, url):
        """
        remove useless url and complete shortened url
        :param url: url to be sanitized
        :return: sanitized url
        """
        if url == "" or url[
            0] == "#":  # remove empty links and don't care about anchor links that lead to the same page
            return None
        if url[0] == "/":  # transform shortened url into full url
            return self.base_url + url[1:]
        return url
