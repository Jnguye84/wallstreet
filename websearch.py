import pandas as pd
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
import mostfrequent
from urllib.request import Request, urlopen

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)

# Set the User-Agent header to mimic a web browser
req = Request(
    url='', #this is where the variable needs to go
    headers={'User-Agent': 'Mozilla/5.0'}
)
webpage = urlopen(req).read()
article_str = text_from_html(webpage)
article = mostfrequent.Keyword(article_str)
article.keyword_list()
article_ = article.keyword_list
print(article_)


