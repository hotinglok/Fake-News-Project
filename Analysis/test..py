from article_scrapers import bbc, guardian, sky, daily_mail
from analysis_utils import keywords
from DocSim import Comparison as ds

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

sentence = link1.body[0]
print(ds.calculate_similarity(sentence, link3.body))