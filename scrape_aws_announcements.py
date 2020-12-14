import requests
from bs4 import BeautifulSoup

year=input("What year do you want to get the new service announcements from? >")

url="https://aws.amazon.com/about-aws/whats-new/"+year+"/"
page=requests.get(url)
soup=BeautifulSoup(page.content,'html.parser')
find_links=soup.find_all('a')
finalarray=[]
for link in find_links:
    if len(link.contents)>0:
        if "INTRODUCING AWS" in str(link.contents[0]).upper() or "INTRODUCING AMAZON" in str(link.contents[0]).upper():
            finalarray.append(str(link.contents[0]))


with open("AWS_"+year+"_NEW_SERVICES.csv","a") as f:
    for item in finalarray:
        f.write("%s\n" % item)


print("Done! File: AWS_"+str(year)+"_NEW_SERVICES.csv")
