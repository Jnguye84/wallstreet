import pandas as pd
from collections import Counter
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
stopwords = stopwords.words("english")
from corextopic import corextopic as ct
from sklearn.feature_extraction.text import TfidfVectorizer

df = pd.read_excel('fake_edited.xlsx')

def Corex(df): #this is to create topics and classify the documents as such
    vectorizer = TfidfVectorizer(
    max_df=.9,
    min_df=3,
    max_features=None,
    ngram_range=(1, 2),
    norm=None,
    binary=True,
    use_idf=False,
    sublinear_tf=False
    )
    vectorizer = vectorizer.fit(df['Text'])
    tfidf = vectorizer.transform(df['Text'])
    vocab = vectorizer.get_feature_names()
    anchors = [['movies'],
               ['teens'],
               ['videogames'],
               ['health']]
    anchors = [
    [a for a in topic if a in vocab]
    for topic in anchors
    ]

    model = ct.Corex(n_hidden=8, seed=42)
    model = model.fit(
        tfidf,
        anchors=anchors,
        words=vocab
    )   
    for i, topic_ngrams in enumerate(model.get_topics(n_words=10)):
        topic_ngrams = [ngram[0] for ngram in topic_ngrams if ngram[1] > 0]
        print("Topic #{}: {}".format(i+1, ", ".join(topic_ngrams)))
    
    topic_df = pd.DataFrame(
        model.transform(tfidf), 
        columns=["topic_{}".format(i+1) for i in range(8)]
    ).astype(float)
    topic_df.index = df.index
    df = pd.concat([df, topic_df], axis=1)
    return df

