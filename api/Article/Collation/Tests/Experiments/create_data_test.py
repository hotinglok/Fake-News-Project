from Collation.rss_feeds import sources 
from scrape import scrapeTest, updateTest   # These functions no longer exist, previously used as initial tests to scrape directly from RSS Feeds and updating csvs.
from IPython.display import display
import pandas
import sqlite3 as sql

# Testing getting fresh data with duplicate rows aggregated
""" for source in sources:
    scrapeSource(source).to_csv(source.path,index=False) """

# Testing to_sql .db file outputs
""" df = scrapeTest(sources[1])
connection = sql.connect('test2.db')
df.to_sql('data', connection) """

# Testing adding fresh data to old data
""" test = scrapeTest(sources[1])
df = updateTest(sources[1].path, test) """

# Testing speed of reading big csv
""" df = pandas.read_csv('bigcsv_test.csv')
df = df.reset_index(drop=True) """

# Testing querying between dates
con = sql.connect('test6.db')

start_time = "2021-02-14"
end_time = "2021-02-16"

df1 = pandas.read_sql_query('SELECT * FROM data WHERE pubDate BETWEEN "{}" AND "{}"'.format(start_time, end_time), con)
display(df1) 
