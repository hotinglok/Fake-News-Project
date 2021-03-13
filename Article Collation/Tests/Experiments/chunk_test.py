import pandas as pd
from IPython.display import display

# Testing boolean masks when reading in .csvs in chunks
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