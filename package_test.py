from Article.Analysis.scrapers import bbc, guardian, sky, daily_mail
from Article.Analysis.utils import getKeywords,getQuotes
from Article.Collation.comparison import DocSim
from gensim.models.keyedvectors import KeyedVectors
import re

link1 = bbc("https://www.bbc.co.uk/news/world-europe-56820970")
link2 = guardian("https://www.theguardian.com/society/2021/apr/20/possible-link-between-johnson-johnson-vaccine-and-rare-blood-clots-says-regulator")
link3 = sky("https://news.sky.com/story/covid-19-johnson-johnson-vaccine-could-be-linked-to-rare-blood-clots-eu-medicines-regulator-says-12281344")
link4 = daily_mail("https://www.dailymail.co.uk/news/article-9490365/EU-drug-regulator-prepares-issue-advice-J-J-COVID-shot.html")

links = [link1, link2, link3, link4]

guardian_test = link3.body
dm = link4.body
count = 0
remaining = 1
quote_count = 1
data = getQuotes(link3)
quotes = data.get('quotes')
text = data.get('text')

print("Quotes: ", len(quotes))
print("Sentences: ", len(text))

for sentences in text:
    print(sentences.get('sentence'))
""" for thing in dm[:]:   # [:] Shallow copy the list since I'm manipulating the data as I'm iterating through stuff
    if bool(re.search(r'''\s'|'\s''', thing.get('sentence'))) == False:
        print(thing.get('sentence'))
    elif bool(re.search(r"^'", thing.get('sentence'))) == False:
        print(thing.get('sentence')) """
    

""" for thing in dm[:]:   # [:] Shallow copy the list since I'm manipulating the data as I'm iterating through stuff
    if bool(re.search(r'''/(['"])([A-Za-z]+)\1/''', thing.get('sentence'))) == True:
        quotes.append(thing)
        dm.remove(thing)

for thing in quotes:
    print('{})'.format(quote_count), thing.get('sentence'))
    quote_count = quote_count + 1 """


""" for count, sentence in enumerate(guardian_test):
    if sentence.find('\"') != -1:
        quotes.append(sentence)
        guardian_test.remove(sentence)



for sentence in guardian_test:
    print(sentence)

for sentence in quotes:
    print('{})'.format(quote_count), sentence)
    quote_count = quote_count + 1  """

""" # Headlines test
for link in links:
    print("Headline: ", link.title)

print('------------------------------') """

""" # Body text test
for link in links:
    print(link.body)
    print('=========') """

""" # Keywords test
for link in links:
    article = " ".join(link.body)
    print(keywords(article)) """

""" sentence = link1.body[5]
googlenews_model_path = 'y:/New Volume/Work & School/School/University of York/Year 4/Fake News/Code/Fake-News-Project/Article/Collation/Data/DocSim/GoogleNews-vectors-negative300.bin'
stopwords_path = "y:/New Volume/Work & School/School/University of York/Year 4/Fake News/Code/Fake-News-Project/Article/Collation/Data/DocSim/stopwords_en.txt"
model = KeyedVectors.load_word2vec_format(googlenews_model_path, binary=True)
with open(stopwords_path, 'r') as fh:
    stopwords = fh.read().split(",")
ds = DocSim(model,stopwords=stopwords)
result = ds.calculate_similarity(sentence, link3.body)
for thing in result:
    print(thing) """
