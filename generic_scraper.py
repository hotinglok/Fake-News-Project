import os
import requests
import pandas
from bs4 import BeautifulSoup
from IPython.display import display

# Class to store source data
class Source:
    __slots__ = ['name', 'path', 'rss']
    def __init__(self, name, path, rss):
        self.name = name
        self.path = path
        self.rss = rss

class Feed:
    __slots__ = ['category', 'url']
    def __init__(self, category, url):
        self.category = category
        self.url = url

# Where the data is stored
data_path_prefix = "y:/New Volume/Work & School/School/University of York/Year 4/Fake News/Code/Fake-News-Project/Article Collation/"

# RSS Feeds
# BBC scraped from every feed at 23:57, 08/03/2021 has 268 unique articles across all of them
bbc_rss=[
Feed("home", "https://feeds.bbci.co.uk/news/rss.xml"),
Feed("uk", "https://feeds.bbci.co.uk/news/uk/rss.xml"),
Feed("world", "https://feeds.bbci.co.uk/news/world/rss.xml"),
Feed("business", "https://feeds.bbci.co.uk/news/business/rss.xml"),
Feed("politics", "https://feeds.bbci.co.uk/news/politics/rss.xml"),
Feed("health", "https://feeds.bbci.co.uk/news/health/rss.xml"),
Feed("education", "https://feeds.bbci.co.uk/news/education/rss.xml"),
Feed("science", "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml"),
Feed("technology", "https://feeds.bbci.co.uk/news/technology/rss.xml"),
Feed("entertainment", "https://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml")]

# Guardian scraped from every feed at 23:57, 08/03/2021 has 193 unique articles between home, uk, world, and coronavirus
guardian_rss=[
Feed("home", "https://www.theguardian.com/uk/rss"),
Feed("uk", "https://www.theguardian.com/uk-news/rss"),
Feed("world", "https://www.theguardian.com/world/rss"),
Feed("coronavirus", "https://www.theguardian.com/world/coronavirus-outbreak/rss")]

sky_rss=[
Feed("home", "https://feeds.skynews.com/feeds/rss/home.xml"),
Feed("uk", "https://feeds.skynews.com/feeds/rss/uk.xml"),
Feed("world", "https://feeds.skynews.com/feeds/rss/world.xml"),
Feed("us", "https://feeds.skynews.com/feeds/rss/us.xml"),
Feed("business", "https://feeds.skynews.com/feeds/rss/business.xml"),
Feed("politics", "https://feeds.skynews.com/feeds/rss/politics.xml"),
Feed("technology", "https://feeds.skynews.com/feeds/rss/technology.xml"),
Feed("strange", "https://feeds.skynews.com/feeds/rss/strange.xml")]

daily_mail_rss=[
Feed("home", "https://feeds.bbci.co.uk/news/rss.xml"),
Feed("uk", "https://feeds.bbci.co.uk/news/uk/rss.xml"),
Feed("world", "https://feeds.bbci.co.uk/news/world/rss.xml"),
Feed("business", "https://feeds.bbci.co.uk/news/business/rss.xml"),
Feed("politics", "https://feeds.bbci.co.uk/news/politics/rss.xml"),
Feed("health", "https://feeds.bbci.co.uk/news/health/rss.xml"),
Feed("education", "https://feeds.bbci.co.uk/news/education/rss.xml"),
Feed("science", "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml"),
Feed("technology", "https://feeds.bbci.co.uk/news/technology/rss.xml"),
Feed("entertainment", "https://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml")]

# Sources
bbc = Source("BBC News", os.path.join(data_path_prefix,r'bbc_data.csv'), bbc_rss)
guardian = Source("The Guardian", os.path.join(data_path_prefix,r'guardian_data.csv'), guardian_rss)
sky = Source("Sky News", os.path.join(data_path_prefix,r'sky_data.csv'), sky_rss)
daily_mail = Source("Daily Mail", os.path.join(data_path_prefix,r'daily_mail_data.csv'), daily_mail_rss)
sources = [bbc, guardian, sky, daily_mail]

# Scrape each feed and add them into an array
scraped_data = []
for feed in sources[1].rss:
    rss_response = requests.get(feed.url)
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

    df = pandas.DataFrame(news_items,columns=['title','description','link','pubDate'])
    scraped_data.append(df)

# Concatenate the new data and convert the publish dates to datetime format
new_data = pandas.concat(scraped_data).drop_duplicates().reset_index(drop=True)
new_data['pubDate'] = pandas.to_datetime(new_data.pubDate)
new_data = new_data.sort_values(by='pubDate', ascending=False)
display(new_data)

""" # Read existing Sky News csv and add the new data to it, removing any duplicates.
existing_data = pandas.read_csv("sky_data6.csv")
existing_data['pubDate'] = pandas.to_datetime(existing_data.pubDate)

updated_data = pandas.concat([existing_data, new_data]).drop_duplicates().reset_index(drop=True).sort_values(by='pubDate', ascending=False)
updated_data.to_csv('sky_data_test.csv',index=False) """