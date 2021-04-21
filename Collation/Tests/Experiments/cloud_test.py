import sqlalchemy
import MySQLdb
import pandas
from IPython.display import display
from rss_feeds import sources
from totally_safe_credentials import db_user, db_pass, db_host, db_name

# Trying to connect to Cloud SQL and display what is currently stored.
''' Connecting to Cloud SQL was pretty different to connecting to my local SQLite files. Various connectors
    were tried to see speed/performance (and what would actually just work with the authorisation I have in place). 
    The repository will have missing versions of when I tried with other connectors as they weren't really worth 
    saving. Each one didn't work too well/just didn't work when I tried it.
'''

# SQLAlchemy connection string for mysqlclient (fork of MySQL-Python)
''' mysql+mysqldb://<user>:<password>@<host>[:<port>]/<dbname>'''
connection_string = "mysql+mysqldb://{}:{}@{}/{}".format(db_user,db_pass,db_host,db_name)

# Establishing the connection
con = sqlalchemy.create_engine(connection_string, echo=True)

# Simple loop just to display each table
for source in sources:
    existing_data = pandas.read_sql_query('SELECT * FROM {}'.format(source.table_name), con)
    display(existing_data)

# Adapted from createData (used when the database was first created/empty)
""" for source in sources:
    df = scrapeSource(source)
    df.to_sql('{}'.format(source.table_name), engine, index=False) """


# Other connection string formats for other connectors I tested previously
""" mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]
mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname> """