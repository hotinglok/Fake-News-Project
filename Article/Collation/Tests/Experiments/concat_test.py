import pandas
from bs4 import BeautifulSoup
from IPython.display import display

# Testing concatenation of multiple .csvs/dataframes to test .drop_duplicates()
''' At this point, data was being collected and stored as separate .csv files each time a scrape was performed.
    The issue with scraping from RSS Feeds is that each feed has a different max number of articles available at
    any given time. As a result, scraping every day would often result in many duplicates.
        - This experiment was done to test the .drop_duplciates() function and see if I could group all the .csvs
          I would create into one file.
'''

df2 = pandas.read_csv("guardian_data2.csv")
df3 = pandas.read_csv("guardian_data3.csv")
df4 = pandas.read_csv("guardian_data4.csv")
df5 = pandas.read_csv("guardian_data5.csv")
df6 = pandas.read_csv("guardian_data6.csv")

result = pandas.concat([df2,df3,df4,df5,df6]).drop_duplicates().reset_index(drop=True)
result['pubDate'] = pandas.to_datetime(result.pubDate)
result.sort_values(by='pubDate')
sorted_result = result.sort_values(by=['pubDate'], ascending=False)
sorted_result.to_csv('guardian_data.csv',index=False)



