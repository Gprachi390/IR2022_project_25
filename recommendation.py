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
def vec(word2vec,tokens):
    a=np.zeros((100,))
    c=0
    for t in tokens:
        if t in word2vec.wv:
            a+=(word2vec.wv[t])
            c+=1
    return (a/c)

def cosine_sim(scrap_news,w2v,user_vec, n=10):
    dist = cosine_similarity(w2v, user_vec.reshape(1,-1))
    ids = np.argsort(dist.ravel())[::-1][0:n+1]
    df = pd.DataFrame({'Headline':scrap_news['Headline'][ids].values,
                'Description':scrap_news['Description'][ids].values,
                'Cosine Similarity':dist[ids].ravel()})
    return df.iloc[1:,]

#collecting all the user history based on the user-id
def get_user_history(news,df,uid):
    df1=df[df["User ID"]==uid]
    l=list(df1.History)
    #print(l)
    h=[]
    for i in l:
        l1=list(set(i.split()))
        h.extend(l1)
        h=list(set(h))
    #print(h)
    nh=[]
    for i in h:
        id=news.index[news["News ID"]==i].tolist()
        nh.append(news["Title"][id[0]])
    return nh

def recommend(uid,c="all"):
    scrap_news=pd.read_csv("data/category.csv")
    #cat=pd.read_csv("category.csv")
    if(c=="all"):
        df=scrap_news.copy()
    else:
        df=scrap_news[scrap_news["category"]==c]
    news=pd.read_csv('news/MINDsmall_train/news.tsv',header=None,sep='\t')
    news.columns=['News ID',
    "Category",
    "SubCategory",
    "Title",
    "Abstract",
    "URL",
    "Title Entities",
    "Abstract Entities"]
    news=news.drop(["Category","SubCategory","Abstract","URL","Title Entities","Abstract Entities"],axis=1)
    #history of user
    users=pd.read_csv('news/MINDsmall_train/behaviors.tsv',header=None,sep='\t')
    users.columns=['Impression ID',
    "User ID",
    "Time",
    "History",
    "Impressions"]
    users=users.drop(["Impression ID","Time","Impressions"],axis=1)
    scrap_news1=pd.read_csv("data/ScrappedNews.csv")
    scrap_news1['text']=scrap_news1['Headline']+scrap_news1['Description']
    scrap_news1['article']=scrap_news1['text'].apply(lambda x : pre_process(x))
    scrap_news1.isna().dropna()
    #scrap_news1.dropna().astype(np.float32)
    tokens=[t for t in scrap_news1.article]
    word2vec = Word2Vec(tokens)
    scrap_news1['word2vec']= scrap_news1['article'].apply(lambda x: vec(word2vec,x))
    w2v=np.array(list(scrap_news1['word2vec']))
    user_hist=get_user_history(news,users,uid)
    
    # pre-processing and getting word2vec for user history
    user_hist_vec=[]
    for h in user_hist:
        t=pre_process(h)
        v=vec(word2vec,t)
        user_hist_vec.append(v)
    w2v=np.nan_to_num(w2v)
    user_hist=np.nan_to_num(user_hist)
    # getting average vector history
    user_vec=np.mean(user_hist_vec, axis=0)
    rec=pd.DataFrame()
    rec=cosine_sim(scrap_news,w2v,user_vec,10)
    rec.to_csv("data/your_recommendation.csv")