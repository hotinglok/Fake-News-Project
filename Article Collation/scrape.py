import os
import requests
import pandas
import sqlite3 as sql
import datetime
from bs4 import BeautifulSoup
from IPython.display import display
from rss_feeds import sources, isValidURL

# Removes <a> something </a> from any given text. Thanks The Guardian.
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

# Scrape each feed (category) from a given source and concatenate the data into one single dataframe.
def scrapeSource(source):
    # For each available feed a source provides, scrape the data into separate dataframes and add them to a list.
    scraped_data = []
    for feed in source.rss:
        scraped_data.append(scrapeFeed(feed.url, source.name, feed.category))

    # Concatenate each dataframe into one and discard any duplicates.
    new_data = pandas.concat(scraped_data).drop_duplicates().reset_index(drop=True)

    # Find any remaining duplicates with differing categories and put them into a single row.
    new_data = new_data.groupby(['source','title','description','link','pubDate'])['category'].apply(', '.join).reset_index()
    # Convert pubDate column to datetime fomat and sort the final dataframe by time (most recent first).
    new_data['pubDate'] = pandas.to_datetime(new_data.pubDate)
    new_data = new_data.sort_values(by='pubDate', ascending=True).reset_index(drop=True)
    return new_data

# Connect to a SQLite database and return a dataframe
def readData(source, date="none"):
    # SQLite BETWEEN accepts datetime or string inputs.
    # The following start/end times are for date inputted and 1 day before
        # start_time = datetime.datetime.strptime(date, '%Y-%m-%d') - datetime.timedelta(days=1)
        # end_time = start_time + datetime.timedelta(days=2)

    con = sql.connect(source.path)    
    # Added "none" in case all data needed to be read
    if date == "none":
        existing_data = pandas.read_sql_query('SELECT * FROM "{}" ORDER BY pubDate DESC'.format(source.name), con)
    else:
        # The following start/end times are for just the date inputted.
        start_time = datetime.datetime.strptime(date, '%Y-%m-%d')
        end_time = start_time + datetime.timedelta(days=1)
        existing_data = pandas.read_sql_query('SELECT * FROM "{}" WHERE pubDate BETWEEN "{}" AND "{}" ORDER BY pubDate DESC'.format(source.name, start_time, end_time), con)

    con.close()
    return existing_data

# Appends new data to an existing SQLite database
def updateData(file_path, new_data):
    # Read the file and convert the pubDate column into datetime format
    con = sql.connect(file_path)
    existing_data = pandas.read_sql_query('SELECT * FROM data', con)
    existing_data['pubDate'] = pandas.to_datetime(existing_data['pubDate'])
    unique_data = getUniqueData(existing_data, new_data)

    unique_data.to_sql('data', con, index=False, if_exists='append')
    con.close()

# Appends new data to an existing table in a SQLite database
def updateBigDB(file_path, sources):
    con = sql.connect(file_path)
    for source in sources:
        # Table name is always source name
        existing_data = pandas.read_sql_query('SELECT * FROM "{}"'.format(source.name), con)
        new_data = scrapeSource(source)
        unique_data = getUniqueData(existing_data, new_data)
        unique_data.to_sql('{}'.format(source.name), con, index=False, if_exists='append')
    con.close()

# Filters out duplicates between existing and new data
def getUniqueData(existing_data, new_data):
    # Checks link because headlines may be re-used, links will always be unique
    cond = new_data['link'].isin(existing_data['link'])
    unique_data = new_data.drop(new_data[cond].index)
    unique_data = unique_data.reset_index(drop=True)
    return unique_data    

# Creates a new database with a given name with data scraped from respective source
def createData(source, name):
    con = sql.connect('{}.db'.format(name))
    df = scrapeSource(source)
    df.to_sql('data', con, index=False)
    con.close()

# Queries the dataframe to find rows with ANY of the keywords. This is to increase likelihood of finding a related article in this first filter.
def searchData(data, search):
    keywords = search.lower().split()
    keywords_string = "|".join(keywords)
    source_name = data['source'].iloc[0]

    # For each selected column, make all entries lowercase and return true where rows contain keywords.
    ''' Both The Guardian and Sky News have keywords which aren't found in the headline/description. This is especially bad with
        Sky News, who have included keywords (eg. "Covid 19" in "Covid 19: Some headline") on the webpage, but do not include it in the RSS Feed data.
    '''
    if source_name == "The Guardian" or "Sky News":
        query = data['title'].str.lower().str.contains(keywords_string)| \
                data['description'].str.lower().str.contains(keywords_string)| \
                data['link'].str.lower().str.contains(keywords_string)
    else:
        query = data['title'].str.lower().str.contains(keywords_string)| \
                data['description'].str.lower().str.contains(keywords_string)

    # Returns the row index of any matched rows
    matches = query[query].index

    # Add queried data to an array if matches are returned
    matches_df = data.iloc[matches]
    if matches_df.empty == True:
        print("{} has no articles with the keyword(s) in this date range".format(source_name))
    else:
        print("{} has {} article(s) containing the keyword(s)".format(source_name, len(matches_df.index)))
        return matches_df


        

