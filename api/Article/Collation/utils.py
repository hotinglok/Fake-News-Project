import pandas
import datetime
import sqlalchemy
import MySQLdb
from .rss_feeds import sources
from .totally_safe_credentials import db_user, db_pass, db_host, db_name

# Return rows from an SQL database. Can return rows between a specified date or all of them in a table
''' SQL BETWEEN accepts datetime or string inputs.
    The following start/end times are for date inputted and 1 day before. May need in the future.
        start_time = datetime.datetime.strptime(date, '%Y-%m-%d') - datetime.timedelta(days=1)
        end_time = start_time + datetime.timedelta(days=2)
'''
def readData(source, con, date="none", extra_days=False):
    # Added "none" in case all data needed to be read
    if date == "none":
        existing_data = pandas.read_sql_query('SELECT * FROM {} ORDER BY pubDate DESC'.format(source.table_name), con)
    else:
        # The following start/end times are for just the date inputted.
        original_time = datetime.datetime.strptime(date, '%Y-%m-%d')
        if extra_days == True:
            start_time = original_time - datetime.timedelta(days=1)
            end_time = start_time + datetime.timedelta(days=2)
        else:
            start_time = original_time
            end_time = start_time + datetime.timedelta(days=1)            
        existing_data = pandas.read_sql_query('SELECT * FROM {} WHERE pubDate BETWEEN "{}" AND "{}" ORDER BY pubDate DESC'.format(source.table_name, start_time, end_time), con)

    return existing_data

# Queries a dataframe to find rows with ANY of the keywords. This is to increase likelihood of finding a related article in this first filter.
def searchData(data, search, source):
    keywords = search.lower().split()
    keywords_string = "|".join(keywords)
    source_name = source

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
    return matches_df

# Same loop that was previously in main. Converted into a function so I don't need to make multiple connections.
def getData(keywords, date="none", extra_days=False):
    queried_sources = []
    matches = 0
    # Connect to the database
    connection_string = "mysql+mysqldb://{}:{}@{}/{}".format(db_user,db_pass,db_host,db_name)
    con = sqlalchemy.create_engine(connection_string)

    # For each source, search for matches. If no matches exist, do not add dataframe into queried_sources
    for source in sources:
        data = readData(source, con, date, extra_days)
        queried_data = searchData(data, keywords, source.name)
        queried_data = queried_data.astype({'pubDate': 'string'})
        if queried_data.empty == True:
            continue
        else:
            matches = matches + len(queried_data)
            queried_sources.append({"name": source.name, "data": queried_data}) # Tuple for convenience.
    
    if matches > 15:
        print("There are {} articles containing the keywords. The comparison may take a while unless you can specify the headline further.".format(matches))
    return queried_sources
        