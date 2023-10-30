import pandas as pd
import pandas as pd
from bs4 import BeautifulSoup
from bs4.element import Comment
from urllib.request import Request, urlopen
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
stopwords = stopwords.words("english")

import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
stopwords = stopwords.words("english")

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
url='https://www.newyorker.com/magazine/2023/11/06/israel-gaza-war-hamas', #this is where the variable needs to go
headers={'User-Agent': 'Mozilla/5.0'}
)
webpage = urlopen(req).read()
article_str = text_from_html(webpage) #string from the entire webpage

def replaceSpecial(lst):
    lst = str(lst)
    lst = lst.split()
    lst = [i.replace(',','') for i in lst]
    lst = [i.replace(f'.','') for i in lst]
    lst = [i.lower() for i in lst]
    return lst

def CountFrequencyinWords(my_list):
    freq = {}
    for item in my_list:
        if (item in freq):
            freq[item] += 1
        else:
            freq[item] = 1.
    freq = dict(sorted(freq.items(), key=lambda item: (item[1]), reverse = True,))
    return freq

class Keyword:
    def __init__(self,text_col):
        self.text_col = text_col
    def category_lst(self):
        category_lst = replaceSpecial(self.text_col)
        category_lst = CountFrequencyinWords(category_lst)
        self.category_lst = {key: value for key, value in category_lst.items() if key not in stopwords}
       
    def ProbFreq(self):
        self.catTotal = len(self.category_lst.values()) + len(self.category_lst.keys()) 
        probfreq = {}
        for key in self.category_lst.keys():
            probfreq.update({key : (self.category_lst[key] + 1 )/self.catTotal}) #the +1 is there because of phantom values
        probfreq = dict(sorted(probfreq.items(), key=lambda item: (item[1]), reverse = True,))
        probfreq = {k: probfreq[k] for k in list(probfreq)[:10]}
        self.probfreq = probfreq

def final_dict(article_str): 
    a = Keyword(article_str) #input is a string
    a.category_lst()
    a.ProbFreq()
    return a.probfreq

def long_dict_category(pathway): #most frequent keywords
    df = pd.read_excel(pathway)
    df = df.fillna('') #makes it an str so that we can split within the text col
    text_index = df.columns.get_loc('Text')
    words = ''
    for row in range(0,len(df)):
        text_str = df.iloc[row,text_index]
        words = words + text_str
    long_dict = final_dict(words)
    return long_dict

import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

fake = long_dict_category(r'/Users/jessicanguyen/Documents/GitHub/wallstreet_moviesml/wallstreet/fake_edited copy.xlsx')
real = long_dict_category(r"/Users/jessicanguyen/Documents/GitHub/wallstreet_moviesml/wallstreet/True copy.xlsx")

neutr = 1/2
fake_denom = min(list(fake.values()))
real_denom = min(list(real.values()))

def DocClassifyExcel(text): #text should be string, real is the category dict, fake is the category dict
    fake_prob = float(neutr)
    text = text.split()

    real_prob = float(neutr)
    for word in list(real.keys()): #fake classification
        if word in text:
            real_prob = float(real_prob) * real[word]
        else:
            real_prob = float(real_prob) * (real_denom)

    for word in list(fake.keys()): #fake classification
        if word in text:
            fake_prob = float(fake_prob) * fake[word]
        else:
            fake_prob = float(fake_prob) * (fake_denom)
            
    return 'fake classification:', fake_prob,'real classification', real_prob

print(DocClassifyExcel(article_str))