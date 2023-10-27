import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from mostfrequent import *

class TableLen(): #getting the length of the data table to go through each row (extracted text within each file)
    def __init__(self, test_doc_classification_table):
        self.test_doc_classification_table = test_doc_classification_table
    def __len__(self):
        return len(self.test_doc_classification_table)
    
class Histogram(): 
    def __init__(self, test_doc_classification_table, lendf):
        self.test_doc_classification_table = test_doc_classification_table
        self.lendf = lendf
    
    def makeHistogram(self): #creating dictionary with {word: total count of word in specific file}
        dict_total = []
        for row in range(0,self.lendf):
            row_dict = Keyword(self.test_doc_classification_table.iloc[row,0].split())
            row_dict.keyword_dict()
            dict_total.append(row_dict.keyword_dict)
        self.dict_total = dict_total
        
    def result(self): #create histogram that will allow us to see the most used words and their total count within each category. This histogram will be created by a dictionary.
        result = Counter()
        for d in range(0, len(self.dict_total)):
            result =  result + Counter(self.dict_total[d]) #the history dictionary will be {word: total count of word in category}
        self.result = dict(sorted(result.items(), key=lambda item: (item[1]), reverse = True,))
        self.result_short = dict(list(self.result.items())[0:30])

class ProbFreq(): 
    def __init__(self, dict):
        self.dict = dict
    def ProbFreq(self):
        self.catTotal = sum(self.dict.values()) + len(self.dict.keys()) 
        probfreq = {}
        for key in self.dict.keys():
            probfreq.update({key : (self.dict[key] + 1)/self.catTotal}) 
            probfreq = dict(sorted(probfreq.items(), key=lambda item: (item[1]), reverse = True,))
        self.probfreq = probfreq

def SocialNetworkGraph(pathway): #most frequent keywords
    df = pd.read_excel(pathway, dtype='string')
    df = df.fillna('') #makes it an str so that we can split within the text col
    keywords_col = []
    text_index = df.columns.get_loc('Text')
    for row in range(0,len(df)):
        text_col = df.iloc[row,text_index]
        obj = Keyword(text_col)
        obj.keyword_list()
         #gets keywords by frequency and getting rid of special characters
        keywords_col.append(obj.keyword_list)
    df['Keywords'] = keywords_col
    df[['key1','key2','key3', 'key4', 'key5']] = df['Keywords'].str.split(' ',n=4, expand = True)
    un_pivot = pd.melt(df, id_vars = 'Title', value_vars = ['key1','key2', 'key3', 'key4', 'key5'])
    un_pivot = un_pivot.drop("variable", axis = 'columns')
    return df, un_pivot #df will have 5 keyword columns for each row detailing the 5 most common keywords #print un_pivot

def ProbCat(df1, df2): #neutral probability
    df1 = len(df1)
    df2 = len(df2)
    tot = df1 + df2
    df1_prob = df1/ tot
    df2_prob = df2 / tot
    return df1_prob, df2_prob
    
def DocClassifyExcel(text): #file should just be 

    fake = SocialNetworkGraph(r'/Users/jessicanguyen/Documents/GitHub/wallstreet_moviesml/wallstreet/fake_edited copy.xlsx')[1]
    real = SocialNetworkGraph(r"/Users/jessicanguyen/Documents/GitHub/wallstreet_moviesml/wallstreet/True copy.xlsx")[1]

    #making histograms 
    lendf = TableLen(real)
    lendf = len(lendf)

    real_hist = Histogram(real, lendf)
    real_hist.makeHistogram()
    real_hist.dict_total
    real_hist.result()
    real_hist.result = real_hist.result

    lendf = TableLen(fake)
    lendf = len(lendf)

    fake_hist = Histogram(fake, lendf)
    fake_hist.makeHistogram()
    fake_hist.dict_total
    fake_hist.result()
    fake_hist.result = fake_hist.result

    #making probability frequency
    fake_freq = ProbFreq(fake_hist.result)
    fake_freq.ProbFreq()
    a_cat_total = fake_freq.catTotal
    fake_freq = fake_freq.probfreq

    real_freq = ProbFreq(real_hist.result)
    real_freq.ProbFreq()
    e_cat_total = real_freq.catTotal
    real_freq = real_freq.probfreq

    test_text = text #this is the text
    test_text = Keyword(test_text)
    test_text.keyword_list()
    test_text = test_text.keyword_list
    prob = 1
    for word in test_text[0:70]:
        if word in list(real_freq.keys()):
            prob = prob * real_freq[word]
        else:
            prob = prob * (1/e_cat_total)

    prob = ProbCat(real,fake)[0]
    real_classification = prob
    prob = 1
    for word in test_text[0:70]:
        if word in list(fake_freq.keys()):
            prob = prob * fake_freq[word]
        else:
            prob = prob * (1/a_cat_total)
    
    prob = ProbCat(real,fake)[1]
    fake_classification = prob

    arr = {real_classification: 'real classification', fake_classification: 'fake classification'}

    return arr
        
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
    url='https://www.newyorker.com/magazine/2023/10/30/on-marriage-devorah-baum-book-review-the-two-parent-privilege-melissa-kearney', #this is where the variable needs to go
    headers={'User-Agent': 'Mozilla/5.0'}
)
webpage = urlopen(req).read()
article_str = text_from_html(webpage)
print(DocClassifyExcel(article_str))
print()
