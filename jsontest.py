from IPython.display import display
from gensim.models.keyedvectors import KeyedVectors
from Article.Collation.comparison import DocSim
from Article.Collation.utils import getData
from Article.Collation.rss_feeds import sources
import datetime
import pandas

# User input keywords and a date
""" keywords = input("Search for a topic: ") 
date = input("Select a date (YYYY-MM-DD): ") """
keywords = "richard"
date = "2021-04-06"

# Get articles from each source containing keywords at the given date
queried_sources = getData(keywords, date)
data = {}

for source in queried_sources:
    source_name = source.get('name').lower().replace(' ', '_')
    source_data = source.get('data').reset_index().to_dict(orient='records')
    data['{}'.format(source_name)] = source_data