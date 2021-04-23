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
date = "2021-04-08"
extra_days = True

# Get articles from each source containing keywords at the given date
queried_sources = getData(keywords, date, extra_days)

# User input to select a source to choose an article from. Count is there just as a reminder for which number to input for now
count = 0
print("Available sources to choose from: ")
for source in queried_sources:
    print("{}) {}".format(count, source.get('name')))
    count = count + 1

#root_source_input = int(input("Select a source: "))
root_source_input = 0
print("{} selected".format(queried_sources[root_source_input].get('name')))
display(queried_sources[root_source_input].get('data'))

queried_root_source = queried_sources[root_source_input].get('data')
del queried_sources[root_source_input]  # Remove chosen source from list so that it won't compare the root article with articles from the same source.

# Select a root article to compare other articles to
#root_article_input = int(input("Select the index of the article to be used as the root article: "))
root_article_input = 0
root_article_row = queried_root_source.iloc[root_article_input]
print("Root article title from {}: {}".format(root_article_row['source'], root_article_row['title']))

# Doc-sim stuff
print("Calculating similarity with other articles...")
googlenews_model_path = 'y:/New Volume/Work & School/School/University of York/Year 4/Fake News/Code/Fake-News-Project/Article/Collation/Data/DocSim/GoogleNews-vectors-negative300.bin'
stopwords_path = "y:/New Volume/Work & School/School/University of York/Year 4/Fake News/Code/Fake-News-Project/Article/Collation/Data/DocSim/stopwords_en.txt"
model = KeyedVectors.load_word2vec_format(googlenews_model_path, binary=True)
with open(stopwords_path, 'r') as fh:
    stopwords = fh.read().split(",")
ds = DocSim(model,stopwords=stopwords)

results = ds.collateArticles(root_article_row['title'], queried_sources)
print('Objects in results:')
for key in results:
    print(key)
    print(results.get('{}'.format(key)))

""" for source in queried_sources:
    result = ds.calculateSimilarity(root_article_row['title'], source.get('data')) """
