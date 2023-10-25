from PKM_keyword_fin import *
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

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

        #plt.bar(self.result_short.keys(), self.result_short.values())
        #plt.xticks(rotation = 90)

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

def ProbCat(df1, df2, df3): #neutral probability
    df1 = len(df1)
    df2 = len(df2)
    df3 = len(df3)
    tot = df1 + df2 + df3
    df1_prob = df1/ tot
    df2_prob = df2 / tot
    df3_prob = df3 / tot
    return df1_prob, df2_prob, df3_prob
    
def DocClassifyExcel(file, num): #file should just be 

    articles = SocialNetworkGraph(r'/Users/jessicanguyen/Documents/GitHub/PKM/PKM/Training_Data_Doc_Classification.xlsx',2)[1]
    emails = SocialNetworkGraph(r"/Users/jessicanguyen/Documents/GitHub/PKM/PKM/Training_Data_Doc_Classification.xlsx",0)[1]
    determinations = SocialNetworkGraph(r"/Users/jessicanguyen/Documents/GitHub/PKM/PKM/Training_Data_Doc_Classification.xlsx",1)[1]

    lendf = TableLen(emails)
    lendf = len(lendf)

    emails_hist = Histogram(emails, lendf)
    emails_hist.makeHistogram()
    emails_hist.dict_total
    emails_hist.result()
    emails_hist.result = emails_hist.result

    lendf = TableLen(determinations)
    lendf = len(lendf)

    determinations_hist = Histogram(determinations, lendf)
    determinations_hist.makeHistogram()
    determinations_hist.dict_total
    determinations_hist.result()
    determinations_hist.result = determinations_hist.result

    lendf = TableLen(articles)
    lendf = len(lendf)

    articles_hist = Histogram(articles, lendf)
    articles_hist.makeHistogram()
    articles_hist.dict_total
    articles_hist.result()
    articles_hist.result = articles_hist.result


    articles_freq = ProbFreq(articles_hist.result)
    articles_freq.ProbFreq()
    a_cat_total = articles_freq.catTotal
    articles_freq = articles_freq.probfreq

    determinations_freq = ProbFreq(determinations_hist.result)
    determinations_freq.ProbFreq()
    d_cat_total = determinations_freq.catTotal
    determinations_freq = determinations_freq.probfreq

    emails_freq = ProbFreq(emails_hist.result)
    emails_freq.ProbFreq()
    e_cat_total = emails_freq.catTotal
    emails_freq = emails_freq.probfreq


    df = pd.read_excel(file, sheet_name = num)
    df = df.fillna('')
    doc_classify = []
    for row in range(0, len(df)):
        test_text = df.iloc[row,0]
        test_text = Keyword(test_text)
        test_text.keyword_list()
        test_text = test_text.keyword_list

        prob = ProbCat(emails, determinations, articles)[0]

        for word in test_text[0:70]:
            if word in list(emails_freq.keys()):
                prob = prob * emails_freq[word]
            else:
                prob = prob * (1/e_cat_total)

        email_classification = prob

        prob = ProbCat(emails, determinations, articles)[1] #neutral probability 

        for word in test_text[0:70]:
            if word in list(determinations_freq.keys()):
                prob = prob * determinations_freq[word]
            else:
                prob = prob * (1/d_cat_total)

        determination_classification = prob

        prob = ProbCat(emails, determinations, articles)[2]

        for word in test_text[0:70]:
            if word in list(articles_freq.keys()):
                prob = prob * articles_freq[word]
            else:
                prob = prob * (1/a_cat_total)


        article_classification = prob

        arr = {determination_classification: 'determination classification', article_classification: 'article classification', email_classification: 'email classification'}
        arr_max = max(list(arr.keys()))
        arr_prob = arr[arr_max]

        doc_classify.append(arr_prob)

    return doc_classify
        
