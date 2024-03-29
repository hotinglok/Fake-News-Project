from .Analysis.scrapers import getArticle
from .Analysis.utils import getKeywords, getQuotes, getStats
from .Collation.utils import getData
from .Collation.comparison import DocSim
from gensim.models.keyedvectors import KeyedVectors
import os

# DocSim setup
dirname = os.path.dirname(__file__)
stopwords_path = os.path.join(dirname, './Collation/Resources/stopwords_en.txt')
googlenews_model_path = os.path.join(dirname, './Collation/Resources/GoogleNews-vectors-negative300.bin')
model = KeyedVectors.load_word2vec_format(googlenews_model_path, binary=True)
with open(stopwords_path, 'r') as fh:
    stopwords = fh.read().split(",")
ds = DocSim(model,stopwords=stopwords)

# Testing collation results function
def compareHeadlines(keywords, date, extra_days, root_source_input, root_article_input):
    # Get articles from each source containing keywords at the given date
    queried_sources = getData(keywords, date, extra_days)
    queried_root_source = queried_sources[root_source_input].get('data')
    del queried_sources[root_source_input]  # Remove chosen source from list so that it won't compare the root article with articles from the same source.

    # Select a root article to compare other articles to
    root_article_row = queried_root_source.iloc[root_article_input]
    root_article_source = root_article_row['source'].lower().replace(' ', '_')
    root_article = [{'title': root_article_row['title'], 
                    'description': root_article_row['description'], 
                    'link': root_article_row['link'], 
                    'pubDate': root_article_row['pubDate'],
                    'category': root_article_row['category'],
                    'source': root_article_row['source']}]

    results = ds.collateArticles(root_article_row['title'], queried_sources)
    results['{}'.format(root_article_source)] = root_article
    return results

# Final function
def analyseArticles(url1, url2):
    # Distinguish URLs:
    first_source_link = getArticle(url1)
    second_source_link = getArticle(url2)

    # Final payload
    data = {}
    data['first_source'] = {}
    data['second_source'] = {}

    # Get quotes, separate text
    first_quotes = getQuotes(first_source_link)
    second_quotes = getQuotes(second_source_link)
    # Sort quotes
    sorted_quotes = ds.calculateSimilarity('quotations', first_quotes.get('quotes'), second_quotes.get('quotes'))
    # Add quotes to final payload
    data.get('first_source')['sorted_quotations'] = sorted_quotes.get('first_source').get('sorted_quotations')
    data.get('first_source')['unsorted_quotations'] = sorted_quotes.get('first_source').get('unsorted_quotations')
    data.get('second_source')['sorted_quotations'] = sorted_quotes.get('second_source').get('sorted_quotations')
    data.get('second_source')['unsorted_quotations'] = sorted_quotes.get('second_source').get('unsorted_quotations')

    # Get sentences containing numbers from the remaining text, separate from text
    first_stats = getStats(first_quotes.get('text'))
    second_stats = getStats(second_quotes.get('text'))
    # Sort stats
    sorted_stats = ds.calculateSimilarity('stats', first_stats.get('stats'), second_stats.get('stats'))
    # Add stats to final payload
    data.get('first_source')['sorted_stats'] = sorted_stats.get('first_source').get('sorted_stats')
    data.get('first_source')['unsorted_stats'] = sorted_stats.get('first_source').get('unsorted_stats')
    data.get('second_source')['sorted_stats'] = sorted_stats.get('second_source').get('sorted_stats')
    data.get('second_source')['unsorted_stats'] = sorted_stats.get('second_source').get('unsorted_stats')

    # Sort remaining sentences after stats were separated from the text
    sorted_text = ds.calculateSimilarity('text', first_stats.get('text'), second_stats.get('text'))
    # Add sorted and unsorted text to payload
    data.get('first_source')['sorted_text'] = sorted_text.get('first_source').get('sorted_text')
    data.get('first_source')['unsorted_text'] = sorted_text.get('first_source').get('unsorted_text')
    data.get('second_source')['sorted_text'] = sorted_text.get('second_source').get('sorted_text')
    data.get('second_source')['unsorted_text'] = sorted_text.get('second_source').get('unsorted_text')
    
    # Get keywords
    first_keywords = getKeywords(first_source_link.article, 9)
    second_keywords = getKeywords(second_source_link.article, 9)
    # Add keywords to final payload
    data.get('first_source')['keywords'] = first_keywords
    data.get('second_source')['keywords'] = second_keywords

    # Add final details for header info (doesn't require similarity computation)
    data.get('first_source')['headline'] = first_source_link.title
    data.get('first_source')['num_sentences'] = first_source_link.num_sentences
    data.get('first_source')['source'] = first_source_link.name
    data.get('first_source')['date_published'] = str(first_source_link.get_date_published())
    data.get('first_source')['date_modified'] = str(first_source_link.get_date_modified())
    data.get('first_source')['url'] = url1
    data.get('second_source')['headline'] = second_source_link.title
    data.get('second_source')['num_sentences'] = second_source_link.num_sentences
    data.get('second_source')['source'] = second_source_link.name
    data.get('second_source')['date_published'] = str(second_source_link.get_date_published())
    data.get('second_source')['date_modified'] = str(second_source_link.get_date_modified())
    data.get('second_source')['url'] = url2

    return data