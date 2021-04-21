""" from IPython.display import display
from scrape import scrapeSource, createData
from rss_feeds import sources
import pandas
import sqlite3 as sql """
    
""" createData(sources[0], 'bbc_data')
createData(sources[1], 'guardian_data')
createData(sources[2], 'sky_data')
createData(sources[3], 'daily_mail_data') """

""" file_path = 'y:/New Volume/Work & School/School/University of York/Year 4/Fake News/Code/Fake-News-Project/Article Collation/big.db'
con = sql.connect(file_path)
existing_data = pandas.read_sql_query('SELECT * FROM "BBC News"', con)
display(existing_data)
con.close() """
