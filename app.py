import csv
import json
import pandas as pd
from flask import Flask, render_template, request, jsonify
from csv import writer
import scrap_news as sn
import categorize as ct
import recommendation as rec
#from flask_cors import CORS

app = Flask(__name__)
user_id="U13740"

# @app.route('/')
# def content():
#     return render_template('index.html')

@app.route('/', methods = ['POST', 'GET'])
def login():
    s = request.get_json()
    if s is not None:
        user_id=s
        print("User ID : "+user_id)
        with open('sample.json', 'a') as f:
            f.write(s)
    return render_template('login.html')

@app.route("/home.html")
def after():
    data=[]
    #sn.scrap()
    #ct.categorize()
    return render_template('home.html', text=data)

@app.route("/index.html", methods = ['POST', 'GET'])
def salvador():
    data = []
    reco=pd.read_csv("data/your_recommendation.csv")
    head=list(reco["Headline"])
    des=list(reco["Description"])
    for i in range(5):
        data.append(head[i])
        data.append(des[i])
    s = request.get_json()
    if s is not None:
        with open('history.csv', 'a') as f:
            obj=writer(f)
            obj.writerow([user_id,s])
            f.close()

    return render_template('index.html', text=data)

@app.route("/yourrecommendation.html", methods = ['POST', 'GET'])
def yourreco():
    rec.recommend(user_id,"all")
    data = []
    reco=pd.read_csv("data/your_recommendation.csv")
    head=list(reco["Headline"])
    des=list(reco["Description"])
    for i in range(5):
        data.append(head[i])
        data.append(des[i])
    s = request.get_json()
    if s is not None:
        with open('history.csv', 'a') as f:
            obj=writer(f)
            obj.writerow([user_id,s])
            f.close()
    return render_template('yourrecommendation.html', text=data)

@app.route("/politics.html", methods = ['POST', 'GET'])
def polit():
    rec.recommend(user_id,"POLITICS")
    data = []
    reco=pd.read_csv("data/your_recommendation.csv")
    head=list(reco["Headline"])
    des=list(reco["Description"])
    for i in range(5):
        data.append(head[i])
        data.append(des[i])
    s = request.get_json()
    if s is not None:
        with open('history.csv', 'a') as f:
            obj=writer(f)
            obj.writerow([user_id,s])
            f.close()
    return render_template('politics.html', text=data)


@app.route("/education.html", methods = ['POST', 'GET'])
def edu():
    rec.recommend(user_id,"EDUCATION")
    data = []
    reco=pd.read_csv("data/your_recommendation.csv")
    head=list(reco["Headline"])
    des=list(reco["Description"])
    for i in range(5):
        data.append(head[i])
        data.append(des[i])
    s = request.get_json()
    if s is not None:
        with open('history.csv', 'a') as f:
            obj=writer(f)
            obj.writerow([user_id,s])
            f.close()
    return render_template('education.html', text=data)


@app.route("/Entertainment.html", methods = ['POST', 'GET'])
def Enter():
    rec.recommend(user_id,"ENTERTAINMENT")
    data = []
    reco=pd.read_csv("data/your_recommendation.csv")
    head=list(reco["Headline"])
    des=list(reco["Description"])
    for i in range(5):
        data.append(head[i])
        data.append(des[i])
    s = request.get_json()
    if s is not None:
        with open('history.csv', 'a') as f:
            obj=writer(f)
            obj.writerow([user_id,s])
            f.close()
    return render_template('Entertainment.html', text=data)

@app.route("/sports.html", methods = ['POST', 'GET'])
def spor():
    rec.recommend(user_id,"SPORTS")
    data = []
    reco=pd.read_csv("data/your_recommendation.csv")
    head=list(reco["Headline"])
    des=list(reco["Description"])
    for i in range(5):
        data.append(head[i])
        data.append(des[i])
    s = request.get_json()
    if s is not None:
        with open('history.csv', 'a') as f:
            obj=writer(f)
            obj.writerow([user_id,s])
            f.close()
    return render_template('sports.html', text=data)


@app.route("/hotnews.html", methods = ['POST', 'GET'])
def hot():
    rec.recommend(user_id,"hot")
    data = []
    reco=pd.read_csv("data/your_recommendation.csv")
    head=list(reco["Headline"])
    des=list(reco["Description"])
    for i in range(5):
        data.append(head[i])
        data.append(des[i])
    s = request.get_json()
    if s is not None:
        with open('history.csv', 'a') as f:
            obj=writer(f)
            obj.writerow([user_id,s])
            f.close()
    return render_template( 'hotnews.html',text=data)

def save(s):
    print("saved")

if __name__ == '__main__':
    app.run(debug=True)
