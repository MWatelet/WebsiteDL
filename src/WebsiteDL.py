from os import path
from HtmlHandlers import HtmlDownloader, HtmlParser
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlparse


class WebsiteDL:

    def __init__(self, url):
        if url[-1] != "/":                      # to standardize the url format given by the user
            url = url + "/"
        self.base_url = url
        self.table = {}                         # will contain the plan of the website as a m*n table
        domain = urlparse(url).netloc           # name of the site
        dir_path = path.dirname(path.realpath(__file__)) + "/html_files"
        site_path = dir_path + "/" + domain
        self.downloader = HtmlDownloader(site_path)
        self.parser = HtmlParser()
        Path(dir_path).mkdir(parents=True,
                             exist_ok=True)     # creation of the local repository for the html files we'll download
        Path(site_path).mkdir(parents=True, exist_ok=True)

    def run(self):
        """
        initial case of the recursive_search_process to not pass the base_url twice to this class and for better clarity
        """
        self.recursive_search_process(self.base_url)

    def recursive_search_process(self, url):
        """
        recursive search of all the files and links in the website
        :param url: url of the html file to inspect
        """
        self.table[url] = []
        try:
            file_name = self.downloader.download_html(url)      # attempt to download the html file
        except HTTPError as error:
            print(url + " : ", end="")  # error 404, for example, are caught here
            print(error)
            return
        hrefs = self.parser.parse_html(file_name)               # find all the links in the html file
        hrefs = self.standardize_hrefs(hrefs)

        for referenced_url in hrefs:
            self.update_table(url, referenced_url)              # store the fact that this url has a link to this referenced url
            if self.check_referenced_url(referenced_url):
                self.recursive_search_process(referenced_url)   # recursive call

    def update_table(self, url, referenced_url):
        """
        update the table and ensure that there is no duplicates
        """
        if referenced_url not in self.table[url]:
            self.table[url].append(referenced_url)

    def check_referenced_url(self, url):
        """
        check if the url is worth exploring
        """
        # condition 1 : url has not been explored yet
        # condition 2 : url is not containing a media (we are looking for html files only)
        # condition 3 : url does not lead to another website (facebook link for example)
        return url not in self.table.keys() \
               and "." not in url[len(self.base_url):] \
               and self.base_url in url

    def standardize_hrefs(self, hrefs):
        """
        remove useless links and transform some links into full url that we can request
        :param hrefs: list of links to standardize
        :return:
        """
        if "" in hrefs:                                         # remove empty links
            hrefs.remove("")
        hrefs = [href for href in hrefs if "#" != href[0]]      # don't care about anchor links that lead to the same page
                                                                # transform shortened url into full url
        hrefs = list(map(lambda href: self.base_url + href[1:] if href[0] == "/" else href, hrefs))
        return hrefs
