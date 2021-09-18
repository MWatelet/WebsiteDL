from WebsiteDL import WebsiteDL
from ConfigReader import read_config


if __name__ == "__main__":
    url = read_config()
    website_scrapper = WebsiteDL()
    plan = website_scrapper.run(url)
    print(plan)

