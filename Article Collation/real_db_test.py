from scrape import createData, scrapeSource, getUniqueData, updateDB, sortDB
from rss_feeds import sources
from IPython.display import display
import sqlite3 as sql
import pandas

""" scraped_data = scrapeSource(sources[0])
new_data = getUniqueData(sources[0].path, scraped_data)
display(new_data)
updateDB(sources[0].path, new_data) """
sortDB(sources[0].path)

""" con = sql.connect('bbc_data.db')

start_time = "2021-03-12"
end_time = "2021-03-14"

current_data = pandas.read_sql_query('SELECT * FROM data WHERE pubDate BETWEEN "{}" AND "{}"'.format(start_time, end_time), con)

search = "Murray Walker"
keywords = search.lower().split()
keywords_string = "|".join(keywords)

query = current_data['title'].str.lower().str.contains(keywords_string)| \
        current_data['description'].str.lower().str.contains(keywords_string)| \
        current_data['link'].str.lower().str.contains(keywords_string)

# Returns the row index of any matched rows
matches = query[query].index

# Add queried data to an array if matches are returned
matches_df = current_data.iloc[matches]

display(matches_df) """