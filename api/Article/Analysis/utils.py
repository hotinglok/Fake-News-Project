# Parts of this code was originally made by Lucas Ou-Yang (@codelucas) and can be found at https://github.com/codelucas/newspaper/blob/master/newspaper/nlp.py.
# This code is used under the MIT License stated in the repository above.
# Edits have been made for the purposes of this project.

import re
import os

# Open the stopwords file and store as a list of separate words
dirname = os.path.dirname(__file__)
stopwords_path = os.path.join(dirname, './Resources/stopwords_en.txt')
with open(stopwords_path) as f:
    stopwords = [line.rstrip() for line in f]

# Functions
# Keyword Extraction from newspaper3k
def split_words(text):
    """Split a string into array of words
    """
    try:
        text = re.sub(r'[^\w ]', '', text)  # strip special chars
        return [x.strip('.').lower() for x in text.split()]
    except TypeError:
        return None

def getKeywords(article, num_keywords=10):
    """Get the top 10 keywords and their frequency scores ignores blacklisted
    words in stopwords, counts the number of occurrences of each word, and
    sorts them in reverse natural order (so descending) by number of
    occurrences.
    """
    text = " ".join(article)
    
    NUM_KEYWORDS = num_keywords
    text = split_words(text)
    
    text = [x for x in text if x not in stopwords]
    freq = {}
    for word in text:
        if word in freq:
            freq[word] += 1
        else:
            freq[word] = 1

    min_size = min(NUM_KEYWORDS, len(freq))
    keywords = sorted(freq.items(),
                        key=lambda x: (x[1], x[0]),
                        reverse=True)
    keywords = keywords[:min_size]

    data = []
    for pair in keywords:
        data.append({'keyword':pair[0], 'frequency':pair[1]})

    return data

# Utility functions for returning separated/categorised text
def getQuotes(url):
    """Return an object containing quotation from an article and the remaining sentences
    """
    quotes = []
    text = url.body
    for line in text[:]:   # [:] Shallow copy the list since I'm manipulating the data as I'm iterating through stuff
        if url.source != 'daily_mail':
            # If the sentence contains either kind of double quotation, it contains a quotation of some sort
            if bool(re.search(r'[\“\"]', line.get('sentence'))) == True:
                quotes.append(line)
                text.remove(line)
            # If the string begisn with either kind of double quotation mark, it is a quotation
            elif bool(re.search(r'''^“|^"''', line.get('sentence'))) == True:
                quotes.append(line)
                text.remove(line)
        else:
            # If the single quotation mark comes after/right before a blank space, this is a quotation mark, not an apostrophe
            if bool(re.search(r'''\s'|'\s''', line.get('sentence'))) == True:
                quotes.append(line)
                text.remove(line)
            # If the string begisn with a single quotation mark, it is a quotation
            elif bool(re.search(r"^'", line.get('sentence'))) == True:
                quotes.append(line)
                text.remove(line)
    data = {'quotes': quotes, 'text': text}
    return data

def getStats(text):
    """Return an object containing any sentences with a number from an article and the remaining sentences
    """
    stats = []
    for line in text[:]:   # [:] Shallow copy the list since I'm manipulating the data as I'm iterating through stuff
        # If string contains any digit. Originally I thought to try make a complicated regex to filter out 'covid-19' but this is actually useful too.
        if bool(re.search(r'\d', line.get('sentence'))) == True:
            stats.append(line)
            text.remove(line)
    data = {'stats': stats, 'text': text}
    return data