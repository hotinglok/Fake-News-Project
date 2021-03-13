from gensim.models.keyedvectors import KeyedVectors
from DocSim import DocSim
from IPython.display import display
from scrape import scrape_sources
import pandas

# Class to store source data
class Source:
    __slots__ = ['name', 'data']
    def __init__(self, name, data):
        self.name = name
        self.data = data

# Pre-processing sources
bbc = Source("BBC News", pandas.read_csv("bbc_data3.csv"))
guardian = Source("The Guardian", pandas.read_csv("guardian_data3.csv"))
sky_news = Source("Sky News", pandas.read_csv("sky_data3.csv"))
daily_mail = Source("Daily Mail", pandas.read_csv("daily_mail_data3.csv"))

sources = []
sources.extend((bbc, guardian, sky_news, daily_mail))
queried_dfs = []

# Search Query
search = input("Search for a topic: ") 
keywords = search.lower().split()
keywords_string = "|".join(keywords)

# Apply query to every sourcce
for source in sources:
    current_data = source.data
    # For each selected column, make all entries lowercase and return true where rows contain keywords
    query = current_data['title'].str.lower().str.contains(keywords_string)| \
            current_data['description'].str.lower().str.contains(keywords_string)| \
            current_data['link'].str.lower().str.contains(keywords_string)

    # Returns the row index of any matched rows
    matches = query[query].index

    # Add queried data to an array if matches are returned
    matches_df = current_data.iloc[matches]
    if matches_df.empty == True:
        print("{} has no articles with the keyword(s) in this date range".format(source.name))
    else:
        print("{} has {} article(s) containing the keyword(s)".format(source.name, len(matches_df.index)))
        queried_dfs.append(matches_df)

# TODO 2nd Query for articles within date range

# Pre-processing the queried sources so that the entire row is preserved
processed_sources = []
bbc_processed = Source("BBC News", queried_dfs[0])
guardian_processed = Source("The Guardian", queried_dfs[1])
sky_news_processed = Source("Sky News", queried_dfs[2])
daily_mail_processed = Source("Daily Mail", queried_dfs[3])
processed_sources.extend((bbc_processed, guardian_processed, sky_news_processed, daily_mail_processed))

# Select a source to choose an article from
root_source_input = int(input("Select a source:\n 0) BBC\n 1) The Guardian\n 2) Sky News\n 3) Daily Mail\n"))
if root_source_input == "0":
    print("BBC Selected\n")

elif root_source_input == "1":
    print("The Guardian Selected\n")

elif root_source_input == "2":
    print("Sky News Selected\n")

elif root_source_input == "3":
    print("Daily Mail Selected\n")

print("Found articles: ")
queried_root_source = processed_sources[root_source_input]
print(queried_root_source.data)

""" """ # Select an article to compare other articles to
root_article_input = int(input("Select the index of the article to be used as the root article: "))
root_article_row = queried_root_source.data.iloc[root_article_input]
root_article_title = root_article_row['title']
root_article_description = root_article_row['description']
print("Root article title from {}: {}".format(queried_root_source.name, root_article_title))

# Pre-processing other sources for similarity calculation
other_sources = []
for source in processed_sources:
    if source.data.equals(queried_root_source.data):
        continue
    titles = source.data['title']
    processed_titles = titles.astype(str).values.tolist()
    output = Source(source.name, processed_titles)
    other_sources.append(output)

# Doc-sim stuff
print("Calculating similarity with other articles...")
googlenews_model_path = './data/GoogleNews-vectors-negative300.bin'
stopwords_path = "./data/stopwords_en.txt"
model = KeyedVectors.load_word2vec_format(googlenews_model_path, binary=True)
with open(stopwords_path, 'r') as fh:
    stopwords = fh.read().split(",")
ds = DocSim(model,stopwords=stopwords)

# Printing results
for source in other_sources:
    result = ds.calculate_similarity(root_article_title, source.data, 0.5)
    print("{}:".format(source.name))
    if not result:
        print("There were no articles which were similar enough to the root article")
    else:
        print(result[0])




# 1. Get CSVs from RSS feeds: --DONE--
    # Each source has it's own CSV sorted (currently) by:
        # title
        # description
        # link
        # pubDate

# 2. Search the headlines and descriptions for the same story: 
    # Find any potential matches based on if the keyword is in the title/description
        # Filter out completely irrelevant rows if the keyword isn't there at all
            # Search title, headline, and link to see if the word is found at all
    # Ask user to choose a root article. --DONE--

    # Find articles which have at least 0.5 similarity to the headline. --DONE--
    # Ask user confirm if these are about the same thing manually.

# 3. Return links of the chosen articles and store:
    # title, description, and link to articles about the same story
    # time of day searched
    # keywords used