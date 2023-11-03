import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
stopwords = stopwords.words("english")
lst_stop = [',','.','hel','eur0',':','would', '', '2011', '30', '12', '20', '15','mn', '$','ovj','2009', '2005','2006', '&', '%', '2010', '2007', ')', '2008', 'also', '(', '17', '-', f"'s", 'eur', '``', 'oyj'] 
for i in lst_stop: stopwords.append(i)
import pandas as pd

def replaceSpecial(lst):
    lst = str(lst)
    lst = lst.split()
    lst = [i.lower() for i in lst]
    return lst

def CountFrequencyinWords(my_list):
    freq = {}
    for item in my_list:
        if (item in freq):
            freq[item] += 1
        else:
            freq[item] = 1.
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
        probfreq = {k: probfreq[k] for k in list(probfreq)[:90]}
        self.probfreq = probfreq

def final_dict(article_str): 
    a = Keyword(article_str) #input is a string
    a.category_lst()
    a.ProbFreq()
    return a.probfreq

def long_dict_category(pathway, sheet_name): #most frequent keywords
    df = pd.read_excel(pathway, sheet_name=sheet_name)
    df = df.fillna('') #makes it an str so that we can split within the text col
    text_index = df.columns.get_loc('Text')
    words = ''
    for row in range(0,len(df)):
        text_str = df.iloc[row,text_index]
        words = words + text_str
    long_dict = final_dict(words)
    return long_dict


neutr = long_dict_category(r'/Users/jessicanguyen/Documents/GitHub/wallstreet_moviesml/wallstreet/financial_sa copy.xlsx', 'neutral')
neutr_stopwords = list(neutr.keys()) #get rid of these words within the other bias categories

neg = long_dict_category(r'/Users/jessicanguyen/Documents/GitHub/wallstreet_moviesml/wallstreet/financial_sa copy.xlsx', 'negative')
neg_stopwords = list(neg.keys()) #get rid of these words within the other bias categories

pos = long_dict_category(r'/Users/jessicanguyen/Documents/GitHub/wallstreet_moviesml/wallstreet/financial_sa copy.xlsx', 'positive')
pos_stopwords = list(pos.keys()) #get rid of these words within the other bias categories

p_bias = {key: value for key, value in pos.items() if key not in neutr_stopwords}
p_bias = {key: value for key, value in pos.items() if key not in neg_stopwords}

n_bias = {key: value for key, value in neg.items() if key not in neutr_stopwords}
n_bias = {key: value for key, value in neg.items() if key not in pos_stopwords}

un_bias = {key: value for key, value in neutr.items() if key not in pos_stopwords}
un_bias = {key: value for key, value in neutr.items() if key not in neg_stopwords}

