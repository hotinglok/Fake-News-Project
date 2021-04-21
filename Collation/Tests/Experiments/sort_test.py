import timeit

# Testing speed of converting pubDate column into datetime64 via pandas and sorting the data in descending order
setup_code = '''
from rss_feeds import sources 
from scrape import scrapeTest, scrapeTest2
from IPython.display import display
import pandas'''

""" run_code = '''
df = scrapeTest(sources[0])
display(df) ''' """

run_code = '''
df = scrapeTest2(sources[0])
display(df) '''

print(timeit.timeit(setup = setup_code, stmt = run_code, number = 1))