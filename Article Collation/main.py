from gensim.models.keyedvectors import KeyedVectors
from DocSim import DocSim
from IPython.display import display
from db_utils import getData
from rss_feeds import sources
import datetime
import pandas

# User input keywords and a date
keywords = input("Search for a topic: ") 
date = input("Select a date (YYYY-MM-DD): ")

# Get articles from each source containing keywords at the given date
queried_sources = getData(keywords, date)

# User input to select a source to choose an article from
root_source_input = int(input("Select a source:\n 0) BBC\n 1) The Guardian\n 2) Sky News\n 3) Daily Mail\n"))
if root_source_input == "0":
    print("BBC Selected\n")
    display(queried_sources[0])

elif root_source_input == "1":
    print("The Guardian Selected\n")
    display(queried_sources[1])

elif root_source_input == "2":
    print("Sky News Selected\n")
    display(queried_sources[2])

elif root_source_input == "3":
    print("Daily Mail Selected\n")
    display(queried_sources[3])

queried_root_source = queried_sources[root_source_input]
del queried_sources[root_source_input]  # Remove chosen source from list so that it won't compare the root article with articles from the same source.

# Select a root article to compare other articles to
root_article_input = int(input("Select the index of the article to be used as the root article: "))
root_article_row = queried_root_source.iloc[root_article_input]
print("Root article title from {}: {}".format(root_article_row['source'], root_article_row['title']))

# Doc-sim stuff
print("Calculating similarity with other articles...")
googlenews_model_path = 'y:/New Volume/Work & School/School/University of York/Year 4/Fake News/Code/Fake-News-Project/Article Collation/Data/DocSim/GoogleNews-vectors-negative300.bin'
stopwords_path = "y:/New Volume/Work & School/School/University of York/Year 4/Fake News/Code/Fake-News-Project/Article Collation/Data/DocSim/stopwords_en.txt"
model = KeyedVectors.load_word2vec_format(googlenews_model_path, binary=True)
with open(stopwords_path, 'r') as fh:
    stopwords = fh.read().split(",")
ds = DocSim(model,stopwords=stopwords)

for source in queried_sources:
    result = ds.calculateSimilarity(root_article_row['title'], source)
