from .Analysis.scrapers import getArticle
from .Analysis.utils import getKeywords, getQuotes, getStats
from .Collation.comparison import DocSim
from gensim.models.keyedvectors import KeyedVectors

# DocSim setup
googlenews_model_path = 'y:/New Volume/Work & School/School/University of York/Year 4/Fake News/Code/Fake-News-Project/Article/Collation/Data/DocSim/GoogleNews-vectors-negative300.bin'
stopwords_path = "y:/New Volume/Work & School/School/University of York/Year 4/Fake News/Code/Fake-News-Project/Article/Collation/Data/DocSim/stopwords_en.txt"
model = KeyedVectors.load_word2vec_format(googlenews_model_path, binary=True)
with open(stopwords_path, 'r') as fh:
    stopwords = fh.read().split(",")
ds = DocSim(model,stopwords=stopwords)

# Final function
def analyseArticles(url1, url2):
    # Distinguish URLs:
    first_source_link = getArticle(url1)
    second_source_link = getArticle(url2)

    # Final payload
    data = {}

    # Get quotes, separate text
    first_quotes = getQuotes(first_source_link)
    second_quotes = getQuotes(second_source_link)
    # Sort quotes
    sorted_quotes = ds.calculateSimilarity('quotations', first_quotes.get('quotes'), second_quotes.get('quotes'))
    # Add quotes to final payload
    data['first_source'] = sorted_quotes.get('first_source')
    data['second_source'] = sorted_quotes.get('second_source')


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

    # Add final details
    data.get('first_source')['headline'] = first_source_link.title
    data.get('first_source')['num_sentences'] = first_source_link.num_sentences
    data.get('second_source')['headline'] = second_source_link.title
    data.get('second_source')['num_sentences'] = second_source_link.num_sentences

    return data