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
""" setup_code = '''
from rss_feeds import sources 
from scrape import scrapeSource, updateDataAppend
from IPython.display import display
import sqlite3 as sql
import pandas'''

run_code = '''
for source in sources:
    new_data = scrapeSource(source)
    updateDataAppend(source.path, new_data)
''' """

# Updating a big db - Two days of data missing, function updates all sources in perfect order: 13.6422431
""" setup_code = '''
from rss_feeds import sources 
from scrape import updateBigDB
import sqlite3 as sql
import pandas'''

run_code = '''
file_path = 'y:/New Volume/Work & School/School/University of York/Year 4/Fake News/Code/Fake-News-Project/Article Collation/big.db'
updateBigDB(file_path, sources)
''' """

# Updating multiple dbs - Two days of data missing, same conditions as above (same date of creation): 12.8425415
setup_code = '''
from rss_feeds import sources 
from scrape import scrapeSource, updateDataAppend
import sqlite3 as sql
import pandas'''

run_code = '''
for source in sources:
    new_data = scrapeSource(source)
    updateDataAppend(source.path, new_data)
'''

print(timeit.timeit(setup = setup_code, stmt = run_code, number = 1))