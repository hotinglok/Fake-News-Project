import os
import requests
import pandas
import re
from bs4 import BeautifulSoup
from IPython.display import display
from rss_feeds import sources, isValidURL

# Returns scraped data from a given RSS Feed XML file as a pandas dataframe.
def scrapeData(url, source_name, category):
    rss_response = requests.get(url)
    soup = BeautifulSoup(rss_response.content, features="xml")

    items = soup.findAll("item")
    news_items = []
    for item in items:
        news_item = {}
        news_item['source'] = source_name
        news_item['title'] = item.title.text
        news_item['description'] = item.description.text
        if source_name == "The Guardian":
            # /video/
            description_soup = BeautifulSoup(news_item['description'], 'html.parser')
            a_tag = description_soup.a
            a_tag.decompose()
            news_item['description'] = description_soup.get_text()
        news_item['link'] = item.link.text
        news_item['pubDate'] = item.pubDate.text
        news_item['category'] = category
        news_items.append(news_item)

    return pandas.DataFrame(news_items,columns=['source','title','description','link','pubDate','category'])

# Returns scraped data from a given RSS Feed XML file as a pandas dataframe.
def test(url, source_name, category):
    rss_response = requests.get(url)
    soup = BeautifulSoup(rss_response.content, features="xml")

    items = soup.findAll("item")
    news_items = []
    for item in items:
        news_item = {}
        if source_name == "The Guardian":
            if isValidURL(item.link.text) == False:
                continue
            elif "|" in item.title.text:
                continue
            description_soup = BeautifulSoup(item.description.text , 'html.parser')
            a_tag = description_soup.a
            a_tag.decompose()
            news_item['description'] = description_soup.get_text()
        else:
            news_item['description'] = item.description.text      
        news_item['source'] = source_name
        news_item['title'] = item.title.text
        news_item['link'] = item.link.text
        news_item['pubDate'] = item.pubDate.text
        news_item['category'] = category
        news_items.append(news_item)

   # return pandas.DataFrame(shit,columns=['source','title','description','link','pubDate','category'])
    return pandas.DataFrame(news_items,columns=['source','title','description','link','pubDate','category'])

# Scrape each feed and add them into an array
def scrapeTest(source):
    # For each available feed a source provides, scrape the data into separate dataframes and add them to a list
    scraped_data = []
    for feed in source.rss:
        scraped_data.append(test(feed.url, source.name, feed.category))

    # Concatenate each dataframe into one and discard any duplicates
    new_data = pandas.concat(scraped_data).drop_duplicates().reset_index(drop=True)

    # Find any remaining duplicates with differing categories and put them into a single row
    new_data = new_data.groupby(['source','title','description','link','pubDate'])['category'].apply(', '.join).reset_index()

    # Convert pubDate column to datetime fomat and sort the final dataframe by time (most recent first)
    new_data['pubDate'] = pandas.to_datetime(new_data.pubDate)
    new_data = new_data.sort_values(by='pubDate', ascending=False)
    return new_data

# Scrape each feed and add them into an array
def scrapeSource(source):
    # For each available feed a source provides, scrape the data into separate dataframes and add them to a list
    scraped_data = []
    for feed in source.rss:
        scraped_data.append(scrapeData(feed.url, source.name, feed.category))

    # Concatenate each dataframe into one and discard any duplicates
    new_data = pandas.concat(scraped_data).drop_duplicates().reset_index(drop=True)

    # Find any remaining duplicates with differing categories and put them into a single row
    new_data = new_data.groupby(['source','title','description','link','pubDate'])['category'].apply(', '.join).reset_index()

    # Convert pubDate column to datetime fomat and sort the final dataframe by time (most recent first)
    new_data['pubDate'] = pandas.to_datetime(new_data.pubDate)
    new_data = new_data.sort_values(by='pubDate', ascending=False)
    return new_data

def updateData(file_path, new_data):
    # Read the file and convert the pubDate column into datetime format
    existing_data = pandas.read_csv(file_path)
    existing_data['pubDate'] = pandas.to_datetime(existing_data.pubDate)

    # Concatenate new data and existing data whilst removing duplicates and sorting by time (most recent first)
    updated_data = pandas.concat([existing_data, new_data]).drop_duplicates().reset_index(drop=True).sort_values(by='pubDate', ascending=False)
    updated_data.to_csv(file_path,index=False)

def scrapeAllSources():
    for source in sources:
        display(scrapeSource(source))
        

