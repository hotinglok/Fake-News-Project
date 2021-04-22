import re
import os

""" here = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(here, 'stopwords-en.txt') """

# Open the stopwords file and store as a list of separate words
stopwords_path = 'y:/New Volume/Work & School/School/University of York/Year 4/Fake News/Code/Fake-News-Project/Article/Analysis/Resources/stopwords-en.txt'
with open(stopwords_path) as f:
    stopwords = [line.rstrip() for line in f]

# Functions
def split_words(text):
    """Split a string into array of words
    """
    try:
        text = re.sub(r'[^\w ]', '', text)  # strip special chars
        return [x.strip('.').lower() for x in text.split()]
    except TypeError:
        return None


def getKeywords(text, num_keywords=10):
    """Get the top 10 keywords and their frequency scores ignores blacklisted
    words in stopwords, counts the number of occurrences of each word, and
    sorts them in reverse natural order (so descending) by number of
    occurrences.
    """
    NUM_KEYWORDS = num_keywords
    text = split_words(text)
    # of words before removing blacklist words

    #num_words = len(text)
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
    keywords = dict((x, y) for x, y in keywords)
    return keywords

"""         for k in keywords:
            articleScore = keywords[k] * 1.0 / max(num_words, 1)
            keywords[k] = articleScore * 1.5 + 1
        return dict(keywords) """

def getQuotes(url):
    """Return an object containing quotations from an article and the remaining sentences
    """
    quotes = []
    text = url.body
    for line in text[:]:   # [:] Shallow copy the list since I'm manipulating the data as I'm iterating through stuff
        if url.source != 'daily_mail':
            if bool(re.search(r'[\“\"]', line.get('sentence'))) == True:
                quotes.append(line)
                text.remove(line)
        else:
            if bool(re.search(r'''\s'|'\s''', line.get('sentence'))) == True:
                quotes.append(line)
                text.remove(line)
                continue
            elif bool(re.search(r"^'", line.get('sentence'))) == True:
                quotes.append(line)
                text.remove(line)
                continue
    data = {'quotes': quotes, 'text': text}
    return data