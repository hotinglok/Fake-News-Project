import timeit

# Testing how quickly data can be returned.
setup_code = '''
from IPython.display import display
from scrape import readData, searchData
from rss_feeds import sources
import pandas
import sqlite3 as sql'''

run_code = '''
data = readData(sources[0].path, "2021-03-16", "2021-03-17")
output = searchData(data, "South Korea")
display(output)
'''

print(timeit.timeit(setup = setup_code, stmt = run_code, number = 1))
