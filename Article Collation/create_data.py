from rss_feeds import sources 
from scrape import scrapeSource
from IPython.display import display
import pandas

""" for source in sources:
    scrapeSource(source).to_csv(source.path,index=False) """

scrapeSource(sources[1]).to_csv("stuff.csv",index=False)
#getNewData(sources[1]).to_csv('skip_test.csv', index = False)

""" import timeit

setup_code = '''
from rss_feeds import sources 
from scrape import scrapeSource
from IPython.display import display'''

run_code = '''
scrapeSource(sources[1]).to_csv('category_test.csv',index=False)'''

print(timeit.timeit(setup = setup_code, stmt = run_code, number = 1)) """
