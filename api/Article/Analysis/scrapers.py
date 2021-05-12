import requests
import re
import json
from datetime import datetime
from bs4 import BeautifulSoup as bs

def isPhraseIn(phrase, text):
    return re.search(r"\b{}\b".format(phrase), text, re.IGNORECASE) is not None

def getArticle(url):
    if 'www.bbc' in url:
        return bbc(url)

    elif 'www.theg' in url:
        return guardian(url)

    elif 'news.sky' in url:
        return sky(url)

    elif 'www.dail' in url:
        return daily_mail(url)

# Separate clasess for each scraper. Returns body text without captions or other artifacts and the headline.
class bbc:
    def __init__(self, url:str):
        article = requests.get(url)
        self.soup = bs(article.content, "html.parser")
        self.body = self.get_body()
        self.article = self.get_article()
        self.title = self.get_title()
        self.num_sentences = len(self.get_body())
        self.date_published = self.get_date_published()
        self.date_modified = self.get_date_modified()
        self.source = 'bbc'
        self.name = 'BBC News'
        
    def get_body(self) -> list:
        body = self.soup.find('article')
        sentences = []
        count = 1
        for p in body.find_all(class_='ssrcss-18snukc-RichTextContainer'):
            if p.find(class_="ssrcss-1pzprxn-BulletListContainer e5tfeyi0"):
                continue
            else:
                sentences.append({'sentence': p.text, 'index': count})
                count = count + 1
        return sentences
    
    def get_article(self) -> list:
        body = self.soup.find('article')
        sentences = []
        for p in body.find_all(class_='ssrcss-18snukc-RichTextContainer'):
            if p.find(class_="ssrcss-1pzprxn-BulletListContainer e5tfeyi0"):
                continue
            else:
                sentences.append(p.text)
        return sentences

    def get_title(self) -> str:
        return self.soup.find(class_="ssrcss-1pl2zfy-StyledHeading e1fj1fc10").text

    def get_date_published(self):
        data = self.soup.find('script', type='application/ld+json').string
        output = json.loads(data)
        date = output['datePublished']
        return date

    def get_date_modified(self):
        data = self.soup.find('script', type='application/ld+json').string
        output = json.loads(data)
        date = output['dateModified']
        return date

class guardian:
    def __init__(self, url:str):
        article = requests.get(url)
        self.soup = bs(article.content, "html.parser")
        self.body = self.get_body()
        self.article = self.get_article()
        self.title = self.get_title()
        self.num_sentences = len(self.get_body())
        self.date_published = self.get_date_published()
        self.date_modified = self.get_date_modified()
        self.source = 'guardian'
        self.name = 'The Guardian'
        
    def get_body(self) -> list:
        body = self.soup.find(class_="article-body-commercial-selector css-79elbk article-body-viewer-selector")
        for p in body.find_all("p", {'id':'sign-in-gate'}): # Removes sign-in-gate <p/> entirely as the index still counts it even when skipped below. 
            p.decompose()
        sentences = []
        count = 1
        for p in body:
            if p.text ==' ' or p.text =='': # Guardian has a strange <p> block with no contents called 'sign-in-gate'.
                continue
            else:
                sentences.append({'sentence': p.text, 'index': count})
                count = count + 1
        return sentences

    def get_article(self) -> list:
        body = self.soup.find(class_="article-body-commercial-selector css-79elbk article-body-viewer-selector")
        for p in body.find_all("p", {'id':'sign-in-gate'}): # Removes sign-in-gate <p/> entirely as the index still counts it even when skipped below. 
            p.decompose()
        sentences = []
        for index, p in enumerate(body):
            if p.text ==' ' or p.text =='': # Guardian has a strange <p> block with no contents called 'sign-in-gate'.
                continue
            else:
                sentences.append(p.text)
        return sentences
    
    def get_title(self) -> str:
        return self.soup.find(class_="css-7g0r1e").text

    def get_date_published(self):
        data = self.soup.find('script', type='application/ld+json').string
        output = json.loads(data)
        date = output[0]['datePublished']   # Guardian is the only source with a strange response for this kind of data
        return date   

    def get_date_modified(self):
        data = self.soup.find('script', type='application/ld+json').string
        output = json.loads(data)
        date = output[0]['dateModified']
        return date  

class sky:
    def __init__(self, url:str):
        article = requests.get(url)
        self.soup = bs(article.content, "html.parser")
        self.body = self.get_body()
        self.article = self.get_article()
        self.title = self.get_title()
        self.num_sentences = len(self.get_body())
        self.date_published = self.get_date_published()
        self.date_modified = self.get_date_modified()
        self.source = 'sky'
        self.name = 'Sky News'

    def get_body(self) -> list:
        body = self.soup.find(class_="sdc-article-body sdc-article-body--story sdc-article-body--lead")
        sentences = []
        count = 1
        for p in body.find_all('p'):
            if p.text ==' ' or p.text =='': # Random gap, not sure where it is.
                continue
            elif isPhraseIn('live updates from the UK and around the world', p.text) == True:
                continue
            else:
                sentences.append({'sentence': p.text, 'index': count})
                count = count + 1
        return sentences

    def get_article(self) -> list:
        body = self.soup.find(class_="sdc-article-body sdc-article-body--story sdc-article-body--lead")
        sentences = []
        for index, p in enumerate(body.find_all('p')):
            if p.text ==' ' or p.text =='': # Random gap, not sure where it is.
                continue
            elif isPhraseIn('live updates from the UK and around the world', p.text) == True:
                continue
            else:
                sentences.append(p.text)
        return sentences
    
    def get_title(self) -> str:
        return self.soup.find(class_="sdc-article-header__long-title").text

    def get_date_published(self):
        data = self.soup.find('script', type='application/ld+json').string
        output = json.loads(data)
        date = output['datePublished']
        return date

    def get_date_modified(self):
        data = self.soup.find('script', type='application/ld+json').string
        output = json.loads(data)
        date = output['dateModified']
        return date

class daily_mail:
    def __init__(self, url:str):
        article = requests.get(url)
        self.soup = bs(article.content, "html.parser")
        self.body = self.get_body()
        self.article = self.get_article()
        self.title = self.get_title()
        self.num_sentences = len(self.get_body())
        self.date_published = self.get_date_published()
        self.date_modified = self.get_date_modified()
        self.source = 'daily_mail'
        self.name = 'Daily Mail'
        
    def get_body(self) -> list:
        body = self.soup.find('div', attrs={'itemprop':"articleBody"})
        # Daily Mail has 'fact box news' blocks with extra information. As these summaries and extra bits aren't present in other sources, they are excluded
        for div in body.find_all('div', attrs={'class':'art-ins mol-factbox news', 'class':'art-ins mol-factbox floatRHS news'}):
            div.decompose()

        sentences = []
        count = 1
        for p in body.find_all('p', attrs={'class':"mol-para-with-font"}):
            sentences.append({'sentence': p.text, 'index': count})
            count = count + 1
        return sentences

    def get_article(self) -> list:
        body = self.soup.find('div', attrs={'itemprop':"articleBody"})
        # Daily Mail has 'fact box news' blocks with extra information. As these summaries and extra bits aren't present in other sources, they are excluded
        for div in body.find_all('div', attrs={'class':'art-ins mol-factbox news', 'class':'art-ins mol-factbox floatRHS news'}):
            div.decompose()

        sentences = []
        for index, p in enumerate(body.find_all('p', attrs={'class':"mol-para-with-font"})):
            sentences.append(p.text)
        return sentences
    
    def get_title(self) -> str:
        return self.soup.find('h2').text

    def get_date_published(self):
        data = self.soup.find('script', type='application/ld+json').string
        output = json.loads(data)
        date = output['datePublished']
        return date

    def get_date_modified(self):
        data = self.soup.find('script', type='application/ld+json').string
        output = json.loads(data)
        date = output['dateModified']
        return date
