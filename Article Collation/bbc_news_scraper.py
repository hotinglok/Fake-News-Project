import requests
import pandas
from bs4 import BeautifulSoup
from IPython.display import display

home = "https://feeds.bbci.co.uk/news/rss.xml"
uk = "https://feeds.bbci.co.uk/news/uk/rss.xml"
world = "https://feeds.bbci.co.uk/news/world/rss.xml"
business = "https://feeds.bbci.co.uk/news/business/rss.xml"
politics = "https://feeds.bbci.co.uk/news/politics/rss.xml"
health = "https://feeds.bbci.co.uk/news/health/rss.xml"
education = "https://feeds.bbci.co.uk/news/education/rss.xml"
science = "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml"
technology = "https://feeds.bbci.co.uk/news/technology/rss.xml"
entertainment = "https://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml"
feeds = [home,uk,world,business,politics,health,education,science,technology,entertainment]

# Scrape home feed (to be updated maybe)
rss_response = requests.get(home)
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

# Convert publish times to datetime objects
new_data = pandas.DataFrame(news_items,columns=['title','description','link','pubDate'])
new_data['pubDate'] = pandas.to_datetime(new_data.pubDate)
bbc_data = pandas.read_csv('bbc_data.csv')
bbc_data['pubDate'] = pandas.to_datetime(bbc_data.pubDate)

# Read existing BBC News csv and add the new data to it, removing any duplicates and sorting by publish date.
updated_data = pandas.concat([bbc_data, new_data]).drop_duplicates().reset_index(drop=True).sort_values(by='pubDate', ascending=False)
updated_data.to_csv('bbc_data_test.csv',index=False)
