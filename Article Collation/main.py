from gensim.models.keyedvectors import KeyedVectors
from DocSim import DocSim
from IPython.display import display
from scrape import readData, searchData
from rss_feeds import sources
import datetime
import pandas
import sqlite3 as sql

""" The bloc's regulator reiterates its support for the vaccine after some countries suspended its use.
The European Union's medicines agency has said there is "no indication" that Oxford-AstraZeneca's coronavirus vaccine is the cause of reported blood clots. """

# 1) User inputs search, inputs date
# 2) Read data from sqlite within date range, convert to dataframe for each source
# 3) query
# Search Query
keywords = input("Search for a topic: ") 
date = input("Select a date (YYYY-MM-DD): ")
queried_sources = []
for source in sources:
    data = readData(source.path, date)
    queried_data = searchData(data, keywords)
    queried_sources.append(queried_data)
for source in queried_sources:   
    #display(source['description'])
    display(source)

# Select a source to choose an article from
root_source_input = int(input("Select a source:\n 0) BBC\n 1) The Guardian\n 2) Sky News\n 3) Daily Mail\n"))
if root_source_input == "0":
    print("BBC Selected\n")

elif root_source_input == "1":
    print("The Guardian Selected\n")

elif root_source_input == "2":
    print("Sky News Selected\n")

elif root_source_input == "3":
    print("Daily Mail Selected\n")

queried_root_source = queried_sources[root_source_input]
del queried_sources[root_source_input]

# Select an article to compare other articles to
root_article_input = int(input("Select the index of the article to be used as the root article: "))
root_article_row = queried_root_source.iloc[root_article_input]
print("Root article title from {}: {}".format(root_article_row['source'], root_article_row['title']))

""" for index, row in queried_sources[1].iterrows():
    print(row['title']) """

""" """ # Doc-sim stuff
print("Calculating similarity with other articles...")
googlenews_model_path = 'y:/New Volume/Work & School/School/University of York/Year 4/Fake News/Code/Fake-News-Project/Article Collation/Data/DocSim/GoogleNews-vectors-negative300.bin'
stopwords_path = "y:/New Volume/Work & School/School/University of York/Year 4/Fake News/Code/Fake-News-Project/Article Collation/Data/DocSim/stopwords_en.txt"
model = KeyedVectors.load_word2vec_format(googlenews_model_path, binary=True)
with open(stopwords_path, 'r') as fh:
    stopwords = fh.read().split(",")
ds = DocSim(model,stopwords=stopwords)

for source in queried_sources:
    result = ds.calculateSimilarity(root_article_row['title'], source)
