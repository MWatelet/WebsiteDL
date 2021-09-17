from Accessor import Downloader
from Reader import read_config


if __name__ == "__main__":
    url = read_config()
    downloader = Downloader()
    downloader.download_html(url)
