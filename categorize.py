import pandas as pd
import numpy as np
import nltk
import os
import matplotlib.pyplot as plt
import re
import string
import io
import glob
import json
import pickle
import joblib
from sklearn.metrics.pairwise import cosine_similarity  
from sklearn.metrics import pairwise_distances
from sklearn.preprocessing import OneHotEncoder
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from nltk.stem import PorterStemmer
ps = PorterStemmer()

from nltk.stem import WordNetLemmatizer
lem = WordNetLemmatizer()

from gensim.models import Word2Vec

def pre_process(s):
    s=str(s)
    s = s.lower()
    l=len(string.punctuation)
    s = s.translate(s.maketrans(string.punctuation,' '*l,''))
    s = re.sub('[^A-Za-z\s\n ]+', ' ',s)
    
    t = word_tokenize(s)
        
    t = [lem.lemmatize(w) for w in t if w not in stopwords.words('english') and w.isalpha() and len(w.strip())>1]
    return t

# taking word2vec of each article
def vec(tokens,word2vec):
    a=np.zeros((100,))
    c=0
    for t in tokens:
        if t in word2vec.wv:
            a+=(word2vec.wv[t])
            c+=1
    return (a/c)

def convert(df,c):
    l=[]
    for i in df[c].values:
        s=''
        for j in i:
            s+=j.lower()+' '
        l.append(s)
    df[c]=l

def categorize():
    scrap_news=pd.read_csv("data/ScrappedNews.csv")
    scrap_news['text']=scrap_news['Headline']+scrap_news['Description']
    scrap_news['article']=scrap_news['text'].apply(lambda x : pre_process(x))
    tokens=[t for t in scrap_news.article]
    word2vec = Word2Vec(tokens)
    scrap_news['word2vec']= scrap_news['article'].apply(lambda x: vec(x,word2vec))
    #w2v=np.array(list(scrap_news['word2vec']))

    clf = joblib.load('model/svm_clf.pkl')
    convert(scrap_news,'article')
    x=scrap_news['article']
    yp=clf.predict(x)
    scrap_news['category']=yp
    #scrap_news.drop(['text','article'],axis=1)
    scrap_news.to_csv("data/category.csv")