from WebsiteDL import WebsiteDL
from ParamReader import ParamReader

if __name__ == "__main__":
    param_reader = ParamReader()
    url = param_reader.get_url()
    website_scrapper = WebsiteDL(url)
    website_scrapper.run()
    website_graph = website_scrapper.website_urls
    for key in website_graph.keys():
        print(key, end=" : ")
        print(str(website_graph[key]))
