import re
import os

# Open the stopwords file and store as a list of separate words
here = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(here, 'stopwords-en.txt')
with open(filename) as f:
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


def keywords(text, num_keywords=10):
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
