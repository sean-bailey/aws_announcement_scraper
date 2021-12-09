import requests
from bs4 import BeautifulSoup
from transformers import pipeline
import csv
summarizer=pipeline('summarization',model="sshleifer/distilbart-cnn-12-6",tokenizer="sshleifer/distilbart-cnn-12-6")

year=input("What year do you want to get the new service announcements from? >")

url="https://aws.amazon.com/about-aws/whats-new/"+year+"/"
page=requests.get(url)
soup=BeautifulSoup(page.content,'html.parser')
find_links=soup.find_all('a')
finalarray=[]
finallinkdict={}
for link in find_links:
    if len(link.text)>0:
        if "INTRODUCING AWS" in str(link.text).upper() or "INTRODUCING AMAZON" in str(link.text).upper():
            finallinkdict["https:"+str(link.attrs['href'])]={"title":link.text,"summary":""}

#we want summarization as well. Take the links, iterate through them, get the text on the page, put it
#in to the summarizer, and spit out a dictionary.

for key in finallinkdict:
    temppage=requests.get(key)
    tempsoup=BeautifulSoup(temppage.content,'html.parser')
    paralist=tempsoup.findAll('p')
    tempsummary=""
    for paragraph in paralist:
        if paragraph.text.count('.')>0:
            tempsummary+=paragraph.text+" "
    fullsummary=summarizer(tempsummary)[0]['summary_text']
    finallinkdict[key]['summary']=fullsummary


finalarray.append(["Title","Summary","URL"])
for key in finallinkdict:
    temparray=[finallinkdict[key]['title'].replace(","," "),finallinkdict[key]['summary'].replace(","," "),key]
    finalarray.append(temparray)

with open("AWS_"+year+"_NEW_SERVICES.csv","a") as f:
    writer=csv.writer(f)
    writer.writerows(finalarray)
    #for item in finalarray:
    #    f.write("%s\n" % item)


input("Done! File: AWS_"+str(year)+"_NEW_SERVICES.csv. Hit enter to continue...")
