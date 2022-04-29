#Import libraries
from bs4 import BeautifulSoup
import requests
import csv

#News description
def news_description(links):
    i = len(links)
    newsl = []
    while i>0:
        res = requests.get(links.pop())
        soup = BeautifulSoup(res.text, 'lxml')
        news_box = soup.find('div', {'class': 'story-right'})
        all_news = news_box.find_all('p')
        newsv = ""
        #print(all_news[0].getText())
        for j in all_news:
            newsv = newsv+j.getText()
        newsv.replace('’',"'")
        newsl.append(newsv)
        i = i-1
    return newsl

def scrap():
    #List for taking all the urls
    urls = []
    #Taking India Today website top news
    url = 'https://www.indiatoday.in/top-stories'
    urls.append(url)
    i = 15
    # newsl is list of headings of news
    newsl=[]
    # linksl is list of links to news
    linksl=[]
    # datesl is list of dates
    datesl=[]
    while(i>0):  
        res = requests.get(urls.pop())
        soup = BeautifulSoup(res.text, 'lxml')
        news_box = soup.find('div', {'class': 'view view-category-wise-content-list view-id-category_wise_content_list view-display-id-section_wise_content_listing view-dom-id- custom'})
        all_news = news_box.find_all('a')
        for news in all_news:
            if news.text == 'next ›':
            #Take Top stories from India Today
                url = 'https://www.indiatoday.in/top-stories'
                url = url.replace('/top-stories',news['href'])
                urls.append(url) 
            elif(len(news.text)>10):
                newsv = news.text
                newsv.replace('’',"'")
                linkv = 'https://www.indiatoday.in'+ news['href']
                datesv = news['href'][-10:len(news['href'])]  
                #print("News :   ",newsv) 
                #print("link : ",linkv) 
                #print("date :  ",datesv)
                newsl.append(newsv)
                linksl.append(linkv)
                datesl.append(datesv)        
        i=i-1

    #Find the total articles
    links_l = linksl[:]
    #Finding discription of each news article
    dis = news_description(links_l)
    dis.reverse()

    articleId = []
    for i in range(1,181):
        articleId.append(i)
    headlinel = list(map(list,zip(articleId, newsl, dis, datesl)))

    #Defining all the columns in the csv file
    columns = ['ArticleId','Headline','Description','Date']

    with open('data/ScrappedNews.csv','w',encoding="utf-8",errors="replace") as fl:
        write = csv.writer(fl,lineterminator = '\n')
        write.writerow(columns)
        write.writerows(headlinel)

