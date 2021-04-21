import pandas as pd
from IPython.display import display

# Testing boolean masks when reading in .csvs in chunks
''' The purpose of this experiment was to see if there was any way of speeding up search/read times.
    Originally, the data was stored as .csvs. The more data that is collected, the larger the file, and the longer it would take 
    to find articles between older dates.
        - In order to deal with this, the data in the .csvs was ordered such that the most recent articles would appear at the top.
          As I expect users to typically search for more recent news, I was trying to see if I could read x amount of lines knowing that
          as soon as a date outside of the range appeared, the .csv reading could be stopped there.
'''

def valid(chunks):
    for chunk in chunks:
        ##chunk['pubDate'] = pandas.to_datetime(chunk['pubDate'])
        mask = chunk['title'] != "Myanmar police surround protesters and raid compound in Yangon"   # Testing with matching strings first
        if mask.all():
            yield chunk
        else:
            yield chunk.loc[mask]
            break

##pd.to_timedelta(chunk['pubDate'], unit='d')
chunksize = 12
chunks = pd.read_csv('chad.csv', chunksize=chunksize, skiprows=30)
df = pd.concat(valid(chunks))
display(df)