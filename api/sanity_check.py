from Article.output import analyseArticles

# Quick test urls for convenience:
link1 = 'https://www.bbc.co.uk/news/uk-scotland-glasgow-west-56821770'
link2 = 'https://www.theguardian.com/lifeandstyle/2021/apr/23/uk-scientists-find-evidence-of-human-to-cat-covid-transmission'

test_results = analyseArticles(link1, link2)
for key in test_results.get('first_source').get('sorted_quotations'):
    print(key)

for key in test_results.get('second_source').get('sorted_quotations'):
    print(key)