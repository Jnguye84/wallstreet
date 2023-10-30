import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from mostfrequent import long_dict_category
 
bias = long_dict_category(r'/Users/jessicanguyen/Documents/GitHub/wallstreet_moviesml/wallstreet/fake_edited copy.xlsx')
un_bias = long_dict_category(r"/Users/jessicanguyen/Documents/GitHub/wallstreet_moviesml/wallstreet/True copy.xlsx")

neutr = 1/2
bias_denom = min(list(bias.values()))
un_bias_denom = min(list(un_bias.values()))

def DocClassifyExcel(text): #text should be string, un_bias is the category dict, bias is the category dict
    bias_prob = float(neutr)
    text = text.split()

    un_bias_prob = float(neutr)
    for word in list(un_bias.keys()): #bias classification
        if word in text:
            un_bias_prob = float(un_bias_prob) * un_bias[word]
        else:
            un_bias_prob = float(un_bias_prob) * (un_bias_denom)

    for word in list(bias.keys()): #bias classification
        if word in text:
            bias_prob = float(bias_prob) * bias[word]
        else:
            bias_prob = float(bias_prob) * (bias_denom)
            
    return 'bias classification:', bias_prob,'un_bias classification', un_bias_prob
