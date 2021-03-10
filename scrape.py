import requests
import pandas
from IPython.display import display
from bs4 import BeautifulSoup


#category = input("Choose a category: ")
#if category == "uk":
 #   bbc_category = "uk/"
 #   guardian_category = ""     

# News Sources
#bbc = "https://feeds.bbci.co.uk/news/{}rss.xml".format(bbc_category)
url = "https://feeds.bbci.co.uk/news/rss.xml"
#

class Source:
    __slots__ = ['name', 'rss_url']
    def __init__(self, name, rss_url):
        self.name = name
        self.rss_url = rss_url

bbc = Source("BBC News", "https://feeds.bbci.co.uk/news/rss.xml")
guardian = Source("guardian", "https://www.theguardian.com/uk/rss")
sky_news = Source("sky", "https://feeds.skynews.com/feeds/rss/uk.xml")
daily_mail = Source("daily_mail", "https://www.dailymail.co.uk/news/index.rss")

sources = []
sources.extend((bbc, guardian, sky_news, daily_mail))

def scrape_sources():
    processed_sources = []
    for source in sources:
        rss_response = requests.get(source.rss_url)
        soup = BeautifulSoup(rss_response.content, features="xml")

        items = soup.findAll("item")
        news_items = []
        for item in items:
            news_item = {}
            news_item['title'] = item.title.text
            news_item['description'] = item.description.text
            news_item['link'] = item.link.text
            news_item['pubDate'] = item.pubDate.text
            news_items.append(news_item)

        data_frame = pandas.DataFrame(news_items,columns=['title','description','link','pubDate'])
        processed_sources.append(data_frame)
    return processed_sources

user_input = input("Scrape all sources or just one to csvs? ")
number_input = input("any number or thing: ")
if user_input == "all":
    for source in sources:
        rss_response = requests.get(source.rss_url)
        soup = BeautifulSoup(rss_response.content, features="xml")

        items = soup.findAll("item")
        news_items = []
        for item in items:
            news_item = {}
            news_item['title'] = item.title.text
            news_item['description'] = item.description.text
            news_item['link'] = item.link.text
            news_item['pubDate'] = item.pubDate.text
            news_item['source'] = source.name
            news_items.append(news_item)

        data_frame = pandas.DataFrame(news_items,columns=['title','description','link','pubDate','source'])
        data_frame.to_csv('test_data_bbc.csv',index=False)

elif user_input == "1":
    source_input = input("bbc_news | guardian | sky_news | daily_mail ")
    if source_input == "bbc_news":
        outlet = bbc
    elif source_input == "guardian":
        outlet = guardian
    elif source_input == "sky_news":
        outlet = sky_news
    elif source_input == "daily_mail":
        outlet = daily_mail

    rss_response = requests.get(outlet.rss_url)
    soup = BeautifulSoup(rss_response.content, features="xml")
    items = soup.findAll("item")
    news_items = []
    for item in items:
        news_item = {}
        news_item['title'] = item.title.text
        news_item['description'] = item.description.text
        news_item['link'] = item.link.text
        news_item['pubDate'] = item.pubDate.text
        news_item['source'] = outlet.name
        news_items.append(news_item)

    data_frame = pandas.DataFrame(news_items,columns=['title','description','link','pubDate','source'])
    data_frame.to_csv('test_data_bbc.csv',index=False)
