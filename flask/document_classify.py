import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from mostfrequent import p_bias, n_bias, un_bias

neutr = 1/3

def DocClassifyExcel(text): #text should be string, un_bias is the category dict, bias is the category dict
    p_bias_prob = float(neutr)
    un_bias_prob = float(neutr)
    n_bias_prob = float(neutr)
    text = text.split()
    list_of_words1 = []
    list_of_words2 = []
    list_of_words3 = []
    lst = []

    for word in list(n_bias.keys()): #negative bias classification
        if word in text:
            n_bias_prob = float(n_bias_prob) * n_bias[word]
            list_of_words1.append(word)
    
    for word in list(un_bias.keys()): #unbias classification
        if word in text:
            un_bias_prob = float(un_bias_prob) * un_bias[word]
            list_of_words2.append(word)

    for word in list(p_bias.keys()): #positive bias classification
        if word in text:
            p_bias_prob = float(p_bias_prob) * p_bias[word]
            list_of_words3.append(word)
    
    arr = {p_bias_prob: 'positive bias classification', un_bias_prob:'un bias classification', n_bias_prob:'negative bias classification'}
    arr_max = max(list(arr.keys()))
    arr_name = arr[arr_max]

    if arr_name == 'positive bias classification':
        lst = list_of_words3
    elif arr_name == 'un bias classification':
        lst = list_of_words2
    elif arr_name == 'negative bias classification':
        lst = list_of_words1
    
    return arr_max, arr_name, lst

