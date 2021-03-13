import pandas
from bs4 import BeautifulSoup
from IPython.display import display

# Testing concatenation of multiple .csvs/dataframes to test .drop_duplicates()
""" df1 = pandas.read_csv("BBC Newsdata1.csv")
df2 = pandas.read_csv("BBCdata1.csv")

test1 = pandas.to_datetime(df1.pubDate)
display(test1)

result = pandas.concat([df1,df2]).drop_duplicates().reset_index(drop=True)
result['pubDate'] = pandas.to_datetime(result.pubDate)
result.sort_values(by='pubDate')
sorted_result = result.sort_values(by=['pubDate'], ascending=False)
sorted_result.to_csv('test_concat6.csv',index=False)
 """

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



