import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
stopwords = stopwords.words("english")

class Keyword:
    def __init__(self,text_col):
        self.text_col = text_col
    def keyword_list(self):
        keyword_list = replaceSpecial(self.text_col)
        self.keyword_list = CountFrequencyinWords(keyword_list)[0]
        self.keyword_list = str([word for word in self.keyword_list if not word in stopwords])
    def keyword_dict(self):
        keyword_dict = replaceSpecial(self.text_col)
        self.keyword_dict = CountFrequencyinWords(keyword_dict)[1]

def replaceSpecial(list):
    list = str(list)
    list = list.lower()
    list = list.split()
    return list

def CountFrequencyinWords(my_list):
    desc_dict = []
    freq = {}
    for item in my_list:
        if (item in freq):
            freq[item] += 1
        else:
            freq[item] = 1.
    freq_sorted_keys = dict(sorted(freq.items(), key=lambda item: (item[1]), reverse = True,))
    for r in freq_sorted_keys:
        desc_dict.append(r)
    return desc_dict, freq_sorted_keys

#the work needed here is brainstorming how to get the bias words from the non-bias words such as names, numbers. Proper nouns are the most likely to be bias as well as descriptive words (adjectives, nouns, verbs).