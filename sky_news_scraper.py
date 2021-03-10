import requests
import pandas
from bs4 import BeautifulSoup
from IPython.display import display

home = "https://feeds.skynews.com/feeds/rss/home.xml"
uk = "https://feeds.skynews.com/feeds/rss/uk.xml"
world = "https://feeds.skynews.com/feeds/rss/world.xml"
us = "https://feeds.skynews.com/feeds/rss/us.xml"
business = "https://feeds.skynews.com/feeds/rss/business.xml"
politics = "https://feeds.skynews.com/feeds/rss/politics.xml"
technology = "https://feeds.skynews.com/feeds/rss/technology.xml"
entertainment = "https://feeds.skynews.com/feeds/rss/entertainment.xml"
strange = "https://feeds.skynews.com/feeds/rss/strange.xml"
feeds = [home,uk,world,us,business,politics,technology,entertainment,strange]

# Scrape each feed and add them into an array
new_data = []
for feed in feeds:
    rss_response = requests.get(feed)
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
    new_data.append(df)

# Concatenate the new data and convert the publish dates to datetime format
output = pandas.concat(new_data).drop_duplicates().reset_index(drop=True)
output['pubDate'] = pandas.to_datetime(output.pubDate)

# Read existing Sky News csv and add the new data to it, removing any duplicates.
sky_news_data = pandas.read_csv("sky_data6.csv")
sky_news_data['pubDate'] = pandas.to_datetime(sky_news_data.pubDate)    # Don't know why it doesn't stay as a datetime object after converting to csv
updated_data = pandas.concat([sky_news_data, output]).drop_duplicates().reset_index(drop=True).sort_values(by='pubDate', ascending=False)
updated_data.to_csv('sky_data_test.csv',index=False)

