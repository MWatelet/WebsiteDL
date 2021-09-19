from WebsiteDL import WebsiteDL
from src.ConfigReader import get_url


if __name__ == "__main__":
    url = get_url()
    website_scrapper = WebsiteDL(url)
    website_scrapper.run()
    plan = website_scrapper.table
    for key in plan.keys():
        print(key, end=" : ")
        print(str(plan[key]))