import pandas
import datetime
import sqlalchemy
import MySQLdb
from rss_feeds import sources
from totally_safe_credentials import db_user, db_pass, db_host, db_name

# Return rows from an SQL database. Can return rows between a specified date or all of them in a table
''' SQL BETWEEN accepts datetime or string inputs.
    The following start/end times are for date inputted and 1 day before. May need in the future.
        start_time = datetime.datetime.strptime(date, '%Y-%m-%d') - datetime.timedelta(days=1)
        end_time = start_time + datetime.timedelta(days=2)
'''
def readData(source, con, date="none"):
    # Added "none" in case all data needed to be read
    if date == "none":
        existing_data = pandas.read_sql_query('SELECT * FROM {} ORDER BY pubDate DESC'.format(source.table_name), con)
    else:
        # The following start/end times are for just the date inputted.
        start_time = datetime.datetime.strptime(date, '%Y-%m-%d')
        end_time = start_time + datetime.timedelta(days=1)
        existing_data = pandas.read_sql_query('SELECT * FROM {} WHERE pubDate BETWEEN "{}" AND "{}" ORDER BY pubDate DESC'.format(source.table_name, start_time, end_time), con)

    return existing_data

# Queries a dataframe to find rows with ANY of the keywords. This is to increase likelihood of finding a related article in this first filter.
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

def getData(keywords, date="none"):
    queried_sources = []
    connection_string = "mysql+mysqldb://{}:{}@{}/{}".format(db_user,db_pass,db_host,db_name)
    con = sqlalchemy.create_engine(connection_string, echo=True)
    for source in sources:
        data = readData(source, con, date)
        queried_data = searchData(data, keywords)
        queried_sources.append(queried_data)
    return queried_sources
        