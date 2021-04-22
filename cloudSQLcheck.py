import sqlalchemy
import MySQLdb
import pandas
from datetime import datetime
from IPython.display import display
from Article.Collation.rss_feeds import sources
from Article.Collation.totally_safe_credentials import db_user, db_pass, db_host, db_name

# Pings the database and returns the length of the table. This shows the total number of articles stored.
''' Connecting to Cloud SQL was pretty different to connecting to my local SQLite files. Various connectors
    were tried to see speed/performance (and what would actually just work with the authorisation I have in place). 
    The repository will have missing versions of when I tried with other connectors as they weren't really worth 
    saving. Each one didn't work too well/just didn't work when I tried it.
'''

# datetime object containing current date and time
now = datetime.now()
# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
print("Current time: ", dt_string)	

# SQLAlchemy connection string for mysqlclient (fork of MySQL-Python)
''' mysql+mysqldb://<user>:<password>@<host>[:<port>]/<dbname>'''
connection_string = "mysql+mysqldb://{}:{}@{}/{}".format(db_user,db_pass,db_host,db_name)

# Establishing the connection
con = sqlalchemy.create_engine(connection_string)

# Simple loop to display number of articles for each source
for source in sources:
    ''' Look back on a specific day '''
    existing_data = pandas.read_sql_query('SELECT * FROM {} WHERE pubDate BETWEEN "2000-04-10" AND "2021-04-11 ORDER BY pubDate ASC"'.format(source.table_name), con)
    ''' Get number of total number of articles '''
    #existing_data = pandas.read_sql_query('SELECT * FROM {}'.format(source.table_name), con)
    print("{}: {}".format(source.name, len(existing_data)))
    #display(existing_data)





# Adapted from createData (used when the database was first created/empty)
""" for source in sources:
    df = scrapeSource(source)
    df.to_sql('{}'.format(source.table_name), engine, index=False) """


# Other connection string formats for other connectors I tested previously
""" mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]
mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname> """