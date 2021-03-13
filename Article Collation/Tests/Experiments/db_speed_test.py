import timeit

# Testing speed of query with SQLite .dbs vs .csvs + Pandas
setup_code = '''
from rss_feeds import sources 
from scrape import scrapeTest, updateTest
from IPython.display import display
import sqlite3 as sql
import pandas'''

run_code = '''
con = sql.connect('test6.db')

start_time = "2021-02-14"
end_time = "2021-02-16"

df1 = pandas.read_sql_query('SELECT * FROM data WHERE pubDate BETWEEN "{}" AND "{}"'.format(start_time, end_time), con)
display(df1) '''

print(timeit.timeit(setup = setup_code, stmt = run_code, number = 1))

""" setup_code = '''
from rss_feeds import sources 
from scrape import scrapeTest, updateTest
from IPython.display import display
import sqlite3 as sql
import pandas'''

run_code = '''
df = pandas.read_csv('bigcsv_test.csv')
query = df['pubDate'].str.contains('2021-02-15 08:57:16+00:00', regex=False)
match = query[query].index
match_df = df.iloc[match]
display(match_df)'''

print(timeit.timeit(setup = setup_code, stmt = run_code, number = 1)) """


