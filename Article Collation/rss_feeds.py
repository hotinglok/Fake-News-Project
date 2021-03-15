import os
import pandas

'''Class to store source data'''
class Source:
    __slots__ = ['name', 'path', 'rss']
    def __init__(self, name, path, rss):
        self.name = name
        self.path = path
        self.rss = rss

'''Class to identify feeds by category'''
class Feed:
    __slots__ = ['category', 'url']
    def __init__(self, category, url):
        self.category = category
        self.url = url

# Where the data is stored
data_path_prefix = "y:/New Volume/Work & School/School/University of York/Year 4/Fake News/Code/Fake-News-Project/Article Collation/Data/News/"

# RSS Feeds
# BBC scraped from every feed at 23:57, 08/03/2021 has 268 unique articles across all of them
bbc_rss=[
Feed("Home", "https://feeds.bbci.co.uk/news/rss.xml"),
Feed("UK", "https://feeds.bbci.co.uk/news/uk/rss.xml"),
Feed("World", "https://feeds.bbci.co.uk/news/world/rss.xml"),
Feed("Business", "https://feeds.bbci.co.uk/news/business/rss.xml"),
Feed("Politics", "https://feeds.bbci.co.uk/news/politics/rss.xml"),
Feed("Health", "https://feeds.bbci.co.uk/news/health/rss.xml"),
Feed("Education", "https://feeds.bbci.co.uk/news/education/rss.xml"),
Feed("Science and Environment", "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml"),
Feed("Technology", "https://feeds.bbci.co.uk/news/technology/rss.xml"),
Feed("Entertainment and Arts", "https://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml")]

# Guardian scraped from every feed at 23:57, 08/03/2021 has 193 unique articles between home, uk, world, and coronavirus
guardian_rss=[
Feed("Home", "https://www.theguardian.com/uk/rss"),
Feed("UK", "https://www.theguardian.com/uk-news/rss"),
Feed("World", "https://www.theguardian.com/world/rss"),
Feed("Coronavirus", "https://www.theguardian.com/world/coronavirus-outbreak/rss"),
Feed("Business", "https://www.theguardian.com/uk/business/rss"),
Feed("Politics", "https://www.theguardian.com/politics/rss"),
Feed("Education", "https://www.theguardian.com/education"),
Feed("Media", "https://www.theguardian.com/media")]

sky_rss=[
Feed("Home", "https://feeds.skynews.com/feeds/rss/home.xml"),
Feed("UK", "https://feeds.skynews.com/feeds/rss/uk.xml"),
Feed("World", "https://feeds.skynews.com/feeds/rss/world.xml"),
Feed("US", "https://feeds.skynews.com/feeds/rss/us.xml"),
Feed("Business", "https://feeds.skynews.com/feeds/rss/business.xml"),
Feed("Politics", "https://feeds.skynews.com/feeds/rss/politics.xml"),
Feed("Technology", "https://feeds.skynews.com/feeds/rss/technology.xml"),
Feed("Offbeat", "https://feeds.skynews.com/feeds/rss/strange.xml")]

daily_mail_rss=[
Feed("News", "https://www.dailymail.co.uk/news/index.rss"),
Feed("Latest News Stories", "https://www.dailymail.co.uk/news/articles.rss"),
Feed("Headlines", "https://www.dailymail.co.uk/news/headlines/index.rss"),
Feed("World News", "https://www.dailymail.co.uk/news/worldnews/index.rss"),
Feed("UK Politics", "https://www.dailymail.co.uk/news/uk-politics/index.rss"),
Feed("Top Science Stories", "https://www.dailymail.co.uk/sciencetech/index.rss"),
Feed("Top Showbiz Stories", "https://www.dailymail.co.uk/tvshowbiz/index.rss")]

# Sources
bbc = Source("BBC News", os.path.join(data_path_prefix,r'bbc_data.db'), bbc_rss)
guardian = Source("The Guardian", os.path.join(data_path_prefix,r'guardian_data.db'), guardian_rss)
sky = Source("Sky News", os.path.join(data_path_prefix,r'sky_data.db'), sky_rss)
daily_mail = Source("Daily Mail", os.path.join(data_path_prefix,r'daily_mail_data.db'), daily_mail_rss)
sources = [bbc, guardian, sky, daily_mail]

# Skip words - RSS Feeds contain live articles which have an entirely different format from regular articles in most cases.
# The Guardian takes this a step further and includes all opinion pieces too, though they often include "| John Doe" to indicate this.
skip_words = ["/live/", "/video/", "/datablog/", "/gallery/", "/keep-connected/", "/picture", "/ng-interactive"]

def isValidURL(url):
    for word in skip_words:
        if word in url:
            return False
    return True