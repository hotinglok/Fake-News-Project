from IPython.display import display
from scrape import scrapeSource, updateDataAppend, readData, createData
from rss_feeds import sources
import pandas
import sqlite3 as sql


""" file_path = 'y:/New Volume/Work & School/School/University of York/Year 4/Fake News/Code/Fake-News-Project/Article Collation/bbc_data.db'
new_data = scrapeSource(sources[0])
updateDataAppend(file_path, new_data) """


file_path = 'y:/New Volume/Work & School/School/University of York/Year 4/Fake News/Code/Fake-News-Project/Article Collation/bbc_data_asc.db'
display(readData(file_path, "2021-03-18"))