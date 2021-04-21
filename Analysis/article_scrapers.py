import requests
from bs4 import BeautifulSoup as bs

# Separate clasess for each scraper. Returns body text without captions or other artifacts and the headline.
class bbc:
    def __init__(self, url:str):
        article = requests.get(url)
        self.soup = bs(article.content, "html.parser")
        self.body = self.get_body()
        self.title = self.get_title()
        
    def get_body(self) -> list:
        body = self.soup.find(class_="ssrcss-5h7eao-ArticleWrapper e1nh2i2l0")
        return [p.text for p in body.find_all('div', attrs={'data-component':"text-block"})]
    
    def get_title(self) -> str:
        return self.soup.find(class_="ssrcss-1pl2zfy-StyledHeading e1fj1fc10").text

class guardian:
    def __init__(self, url:str):
        article = requests.get(url)
        self.soup = bs(article.content, "html.parser")
        self.body = self.get_body()
        self.title = self.get_title()
        
    def get_body(self) -> list:
        body = self.soup.find(class_="article-body-commercial-selector css-79elbk article-body-viewer-selector")
        sentences = []
        for p in body:
            if p.text =='': # Guardian has a strange <p> block with no contents called 'sign-in-gate'.
                continue
            else:
                sentences.append(p.text)
        return sentences
    
    def get_title(self) -> str:
        return self.soup.find(class_="css-1nupfq9").text

class sky:
    def __init__(self, url:str):
        article = requests.get(url)
        self.soup = bs(article.content, "html.parser")
        self.body = self.get_body()
        self.title = self.get_title()
        
    def get_body(self) -> list:
        body = self.soup.find(class_="sdc-article-body sdc-article-body--story sdc-article-body--lead")
        return [p.text for p in body.find_all('p')]
    
    def get_title(self) -> str:
        return self.soup.find(class_="sdc-article-header__long-title").text

class daily_mail:
    def __init__(self, url:str):
        article = requests.get(url)
        self.soup = bs(article.content, "html.parser")
        self.body = self.get_body()
        self.title = self.get_title()
        
    def get_body(self) -> list:
        body = self.soup.find('div', attrs={'itemprop':"articleBody"})
        # Daily Mail has 'fact box news' blocks with extra information. As these summaries and extra bits aren't present in other sources, they are excluded
        for div in body.find_all('div', attrs={'class':'art-ins mol-factbox news'}):
            div.decompose()
        return [p.text for p in body.find_all('p', attrs={'class':"mol-para-with-font"})]
    
    def get_title(self) -> str:
        return self.soup.find('h2').text
