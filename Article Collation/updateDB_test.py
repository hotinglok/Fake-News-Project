import timeit

# Testing speed of updating database (either concat + drop_duplicates() or concat only new unique data)

# concat + drop_duplicates()
""" setup_code = '''
from rss_feeds import sources 
from scrape import scrapeSource, updateData
from IPython.display import display
import sqlite3 as sql
import pandas'''

run_code = '''
new_data = scrapeSource(sources[0])
output = updateData(sources[0].path, new_data)
''' """
# concat unique data only
setup_code = '''
from rss_feeds import sources 
from scrape import scrapeSource, updateData2
from IPython.display import display
import sqlite3 as sql
import pandas'''

run_code = '''
new_data = scrapeSource(sources[0])
output = updateData2(sources[0].path, new_data)
'''

print(timeit.timeit(setup = setup_code, stmt = run_code, number = 1))