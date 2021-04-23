# Timeit code
import timeit

setup_code = '''
from Article.output import analyseArticles'''

run_code = '''
link1 = "https://www.bbc.co.uk/news/uk-politics-56863547"
link2 = "https://www.theguardian.com/politics/2021/apr/23/dominic-cummings-launches-attack-on-boris-johnson"
output = analyseArticles(link1, link2)'''

print(timeit.timeit(setup = setup_code, stmt = run_code, number = 1)) 

# Actual testing code
""" 
from Article.output import analyseArticles

# J&J vaccine blood clots
link1 = "https://www.bbc.co.uk/news/world-europe-56820970"
link2 = "https://news.sky.com/story/covid-19-johnson-johnson-vaccine-could-be-linked-to-rare-blood-clots-eu-medicines-regulator-says-12281344"

# Something about Dominic Cummings and Boris Johnson
link1 = "https://www.bbc.co.uk/news/uk-politics-56863547"
link2 = "https://www.theguardian.com/politics/2021/apr/23/dominic-cummings-launches-attack-on-boris-johnson"

output = analyseArticles(link1, link2)
print(output) """

""" for key in output.get('first_source'):
    print(key)

for key in output.get('second_source'):
    print(key) """