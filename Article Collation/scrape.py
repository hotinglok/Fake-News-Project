import os
import requests
import pandas
import sqlite3 as sql
from bs4 import BeautifulSoup
from IPython.display import display
from rss_feeds import sources, isValidURL

# Removes <a> content </a> from any given text. Thanks The Guardian.
def cleanDescription(text):
    soup = BeautifulSoup(text , 'html.parser')
    a_tag = soup.a
    a_tag.decompose()
    return soup.get_text()

# Returns scraped data from a given RSS Feed XML file as a pandas dataframe.
def scrapeFeed(url, source_name, category):
    rss_response = requests.get(url)
    soup = BeautifulSoup(rss_response.content, features="xml")

    items = soup.findAll("item")
    news_items = []
    for item in items:
        news_item = {}
        if source_name == "Sky News":
            # If "news-live" is in a link, this leads to an article with live updates, hence invalid.
            if "news-live" in item.link.text:
                continue
        if source_name == "The Guardian":
            # Guardian has different slugs in links to indicate differently styled article pages (eg. /video/ or /gallery/).
            if isValidURL(item.link.text) == False:
                continue
            # A "|" in the headline indicates it is an opinion piece.
            elif "|" in item.title.text:
                continue
            news_item['description'] = cleanDescription(item.description.text)
        else:
            news_item['description'] = item.description.text      
        news_item['source'] = source_name
        news_item['title'] = item.title.text
        news_item['link'] = item.link.text
        news_item['pubDate'] = item.pubDate.text
        news_item['category'] = category
        news_items.append(news_item)

    data = pandas.DataFrame(news_items,columns=['source','title','description','link','pubDate','category'])
    return data

# Scrape each feed and add them into an array
def scrapeSource(source):
    # For each available feed a source provides, scrape the data into separate dataframes and add them to a list
    scraped_data = []
    for feed in source.rss:
        scraped_data.append(scrapeFeed(feed.url, source.name, feed.category))

    # Concatenate each dataframe into one and discard any duplicates
    new_data = pandas.concat(scraped_data).drop_duplicates().reset_index(drop=True)

    # Find any remaining duplicates with differing categories and put them into a single row
    new_data = new_data.groupby(['source','title','description','link','pubDate'])['category'].apply(', '.join).reset_index()
    # Convert pubDate column to datetime fomat and sort the final dataframe by time (most recent first)
    new_data['pubDate'] = pandas.to_datetime(new_data.pubDate)
    new_data = new_data.sort_values(by='pubDate', ascending=False).reset_index(drop=True)
    return new_data

""" def updateData(file_path, new_data):
    # Read the file and convert the pubDate column into datetime format
    existing_data = pandas.read_csv(file_path)
    existing_data['pubDate'] = pandas.to_datetime(existing_data.pubDate)

    # Concatenate new data and existing data whilst removing duplicates and sorting by time (most recent first)
    updated_data = pandas.concat([existing_data, new_data]).drop_duplicates().reset_index(drop=True).sort_values(by='pubDate', ascending=False)
    updated_data.to_csv(file_path,index=False) """

def updateTest(file_path, new_data):
    # Read the file and convert the pubDate column into datetime format
    existing_data = pandas.read_csv(file_path)
    existing_data['pubDate'] = pandas.to_datetime(existing_data.pubDate)

    # Concatenate new data and existing data whilst removing duplicates and sorting by time (most recent first)
    updated_data = pandas.concat([existing_data, new_data]).drop_duplicates().reset_index(drop=True).sort_values(by='pubDate', ascending=False)
    return updated_data

def readData(file_path, date):
    end_time = date
    start_time = end_time - 1
    con = sql.connect(file_path)
    existing_data = pandas.read_sql_query('SELECT * FROM data WHERE pubDate BETWEEN "{}" AND "{}"'.format(start_time, end_time), con)
    con.close()
    return existing_data

def updateData(file_path, new_data):
    # Read the file and convert the pubDate column into datetime format
    con = sql.connect(file_path)
    existing_data = pandas.read_sql_query('SELECT * FROM data', con)
    existing_data['pubDate'] = pandas.to_datetime(existing_data['pubDate'])

    # Concatenate new data and existing data whilst removing duplicates and sorting by time (most recent first)
    updated_data = pandas.concat([existing_data, new_data]).drop_duplicates().reset_index(drop=True).sort_values(by='pubDate', ascending=False)
    updated_data.to_sql('data', con, index=False, if_exists='replace')
    con.close()
    return updated_data

def updateData2(file_path, new_data):
    # Read the file and convert the pubDate column into datetime format
    con = sql.connect(file_path)
    existing_data = pandas.read_sql_query('SELECT * FROM data', con)
    existing_data['pubDate'] = pandas.to_datetime(existing_data['pubDate'])
    unique_data = getUniqueData2(existing_data, new_data)

    # Concatenate new data and existing data whilst removing duplicates and sorting by time (most recent first)
    updated_data = pandas.concat([existing_data, unique_data]).reset_index(drop=True).sort_values(by='pubDate', ascending=False)
    updated_data.to_sql('data', con, index=False, if_exists='replace')
    con.close()
    return updated_data

def getUniqueData2(existing_data, new_data):
    # Read the file and convert the pubDate column into datetime format
    cond = new_data['link'].isin(existing_data['link'])
    unique_data = new_data.drop(new_data[cond].index)
    unique_data = unique_data.reset_index(drop=True)
    return unique_data    

def getUniqueData(file_path, new_data):
    # Read the file and convert the pubDate column into datetime format
    con = sql.connect(file_path)
    existing_data = pandas.read_sql_query('SELECT * FROM data', con)
    con.close()
    existing_data['pubDate'] = pandas.to_datetime(existing_data['pubDate'])

    cond = new_data['link'].isin(existing_data['link'])
    unique_data = new_data.drop(new_data[cond].index)
    unique_data = unique_data.reset_index(drop=True)
    return unique_data

def updateDB(file_path, new_data):
    # Read the file and convert the pubDate column into datetime format
    con = sql.connect(file_path)
    cur = con.cursor()
    new_data.to_sql('data', con, index=False, if_exists='append')
    cur.execute('SELECT * FROM data ORDER BY pubDate DESC')
    con.commit()
    con.close()

def sortDB(file_path):
    print(file_path)
    con = sql.connect(file_path)
    cur = con.cursor()
    #cur.execute('SELECT * FROM data ORDER BY pubDate DESC')
    cur.execute('ALTER TABLE data ORDER BY pubDate DESC')
    con.commit()
    con.close()

def createData(source, name):
    con = sql.connect('{}.db'.format(name))
    df = scrapeSource(source)
    df.to_sql('data', con, index=False)
    con.close()
        

