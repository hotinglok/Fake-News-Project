import requests
import re
from bs4 import BeautifulSoup as bs

def isPhraseIn(phrase, text):
    return re.search(r"\b{}\b".format(phrase), text, re.IGNORECASE) is not None

# Separate clasess for each scraper. Returns body text without captions or other artifacts and the headline.
class bbc:
    def __init__(self, url:str):
        article = requests.get(url)
        self.soup = bs(article.content, "html.parser")
        self.body = self.get_body()
        self.title = self.get_title()
        self.source = 'bbc'
        
    def get_body(self) -> list:
        body = self.soup.find(class_="ssrcss-5h7eao-ArticleWrapper e1nh2i2l0")
        sentences = []
        for index, p in enumerate(body.find_all('div', attrs={'data-component':"text-block"})):
            sentences.append({'sentence': p.text, 'position': index})
        return sentences
    
    def get_title(self) -> str:
        return self.soup.find(class_="ssrcss-1pl2zfy-StyledHeading e1fj1fc10").text

class guardian:
    def __init__(self, url:str):
        article = requests.get(url)
        self.soup = bs(article.content, "html.parser")
        self.body = self.get_body()
        self.title = self.get_title()
        self.source = 'guardian'
        
    def get_body(self) -> list:
        body = self.soup.find(class_="article-body-commercial-selector css-79elbk article-body-viewer-selector")
        sentences = []
        for index, p in enumerate(body):
            if p.text =='': # Guardian has a strange <p> block with no contents called 'sign-in-gate'.
                continue
            else:
                sentences.append({'sentence': p.text, 'position': index})
        return sentences
    
    def get_title(self) -> str:
        return self.soup.find(class_="css-1nupfq9").text

class sky:
    def __init__(self, url:str):
        article = requests.get(url)
        self.soup = bs(article.content, "html.parser")
        self.body = self.get_body()
        self.title = self.get_title()
        self.source = 'sky'

    def get_body(self) -> list:
        body = self.soup.find(class_="sdc-article-body sdc-article-body--story sdc-article-body--lead")
        sentences = []
        for index, p in enumerate(body.find_all('p')):
            if p.text ==' ': # Random gap, not sure where it is.
                continue
            elif isPhraseIn('live updates from the UK and around the world', p.text) == True:
                continue
            else:
                sentences.append({'sentence': p.text, 'position': index})
        return sentences
    
    def get_title(self) -> str:
        return self.soup.find(class_="sdc-article-header__long-title").text

class daily_mail:
    def __init__(self, url:str):
        article = requests.get(url)
        self.soup = bs(article.content, "html.parser")
        self.body = self.get_body()
        self.title = self.get_title()
        self.source = 'daily_mail'
        
    def get_body(self) -> list:
        body = self.soup.find('div', attrs={'itemprop':"articleBody"})
        # Daily Mail has 'fact box news' blocks with extra information. As these summaries and extra bits aren't present in other sources, they are excluded
        for div in body.find_all('div', attrs={'class':'art-ins mol-factbox news', 'class':'art-ins mol-factbox floatRHS news'}):
            div.decompose()

        sentences = []
        for index, p in enumerate(body.find_all('p', attrs={'class':"mol-para-with-font"})):
            sentences.append({'sentence': p.text, 'position': index})
        return sentences
    
    def get_title(self) -> str:
        return self.soup.find('h2').text
