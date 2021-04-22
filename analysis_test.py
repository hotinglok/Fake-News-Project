from Article.Analysis.scrapers import bbc, guardian, sky, daily_mail
from Article.Analysis.utils import getKeywords
from Article.Collation.DocSim import DocSim
from gensim.models.keyedvectors import KeyedVectors

link1 = bbc("https://www.bbc.co.uk/news/world-europe-56820970")
link2 = guardian("https://www.theguardian.com/society/2021/apr/20/possible-link-between-johnson-johnson-vaccine-and-rare-blood-clots-says-regulator")
link3 = sky("https://news.sky.com/story/covid-19-johnson-johnson-vaccine-could-be-linked-to-rare-blood-clots-eu-medicines-regulator-says-12281344")
link4 = daily_mail("https://www.dailymail.co.uk/news/article-9490365/EU-drug-regulator-prepares-issue-advice-J-J-COVID-shot.html")

links = [link1, link2, link3, link4]

""" # Headlines test
for link in links:
    print("Headline: ", link.title)

print('------------------------------')

# Body text test
for link in links:
    print(link.body)
    print('=========') """

""" # Keywords test
for link in links:
    article = " ".join(link.body)
    print(keywords(article)) """

sentence = link1.body[5]
googlenews_model_path = 'y:/New Volume/Work & School/School/University of York/Year 4/Fake News/Code/Fake-News-Project/Collation/Data/DocSim/GoogleNews-vectors-negative300.bin'
stopwords_path = "y:/New Volume/Work & School/School/University of York/Year 4/Fake News/Code/Fake-News-Project/Collation/Data/DocSim/stopwords_en.txt"
model = KeyedVectors.load_word2vec_format(googlenews_model_path, binary=True)
with open(stopwords_path, 'r') as fh:
    stopwords = fh.read().split(",")
ds = DocSim(model,stopwords=stopwords)
print(ds.calculate_similarity(sentence, link3.body))