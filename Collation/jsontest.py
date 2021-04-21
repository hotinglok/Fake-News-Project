from gensim.models.keyedvectors import KeyedVectors
from DocSim import DocSim
from IPython.display import display
from db_utils import getData
from rss_feeds import sources
import datetime
import pandas

# User input keywords and a date
""" keywords = input("Search for a topic: ") 
date = input("Select a date (YYYY-MM-DD): ") """
keywords = "richard"
date = "2021-04-06"

# Get articles from each source containing keywords at the given date
queried_sources = getData(keywords, date)

for source in queried_sources:
    #source.get('data').to_json('{}_test'.format(source.get('name'), orient='records', indent=2))
    test = source.get('data').to_dict(orient='records')
    print(test)