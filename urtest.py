from Article.Analysis.scrapers import bbc, guardian, sky, daily_mail
import re

# Tests for url checker function in Article/Analysis/scrapers.py

link1 = "https://www.bbc.co.uk/news/world-europe-56820970"
link2 = "https://www.theguardian.com/society/2021/apr/20/possible-link-between-johnson-johnson-vaccine-and-rare-blood-clots-says-regulator"
link3 = "https://news.sky.com/story/covid-19-johnson-johnson-vaccine-could-be-linked-to-rare-blood-clots-eu-medicines-regulator-says-12281344"
link4 = "https://www.dailymail.co.uk/news/article-9490365/EU-drug-regulator-prepares-issue-advice-J-J-COVID-shot.html"

""" if 'www.bbc' in link4:
    output = bbc(link1).source
else:
    output = 'no'
print(output)

if 'www.theg' in link4:
    output = guardian(link2).source
else:
    output = 'no'
print(output)

if 'news.sky' in link4:
    output = sky(link3).source
else:
    output = 'no'
print(output)

if 'www.dail' in link4:
    output = daily_mail(link4).source
else:
    output = 'no'
print(output) """

string = 'this sentence mentions covid-19'
string2 = 'there were 30 million cases of some deadly disease with covid-19'
# Finds negative matches for '-19', hence tries to find every match containing numbers, except with '-19'
if bool(re.search(r'^(?!.*(-19)).*\d', string)) == True:
    print('dammit')
else:
    print('wat')

if bool(re.search(r'\d', string2)) == True:
    print('dammit')
else:
    print('wat')
