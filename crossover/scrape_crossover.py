# -*- coding: utf-8 -*-
"""
Created on Wed Jan  1 22:48:13 2020

@author: tneha
"""


"""
This code scrapes Harry Potter and its associated cross-overs data from fanfiction.net

It returns a dataframe of edge-list, where:
    'to': fandom 1
    'from': fandom 2 with which fandom1 has cross-overs with
    'number_fanfic': the number of stories with fandom1-fandom2 cross-over

"""


import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


url = "https://www.fanfiction.net/crossovers/Harry-Potter/224/"

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

#on inspecting the page we see that the fanfic data is contained in 'td' tag
l = soup.findAll('td')

#upon parsing the list we find the fanfic data in 3rd element of the list
#within the 3rd 'td' element, each entry is a 'div' tag
l = l[2].findAll('div')


#keeping the top 5 most popular cross-overs for Harry Potter
l = l[:5]


urllist = []
urllist.append(url)

#from the HP cross-over page we need to create url for cross-over pages of the first 5 fandoms extracted above

for item in l:
    code = re.search("224/(.*)", str(item.a['href'])).group(1)
    title = re.search("/Harry-Potter-and-(.*)-Crossovers", str(item.a['href'])).group(1)
    urllist.append("https://www.fanfiction.net/crossovers/"+title+"/"+code)
    
    
#create the dataframe

df = []

#repeat the process for each url and create a list of dict for the dataframe
for link in urllist:
    
    response = requests.get(link)

    soup = BeautifulSoup(response.text, "html.parser")
    
    l = soup.findAll('td')
    l = l[2].findAll('div')
    
    l = l[:5]
    
    #extract the 'from', 'to', and 'number_fanfic' information using regex on html tags
    for item in l:
        
        ff = re.sub("-", " ", re.search("crossovers/([^0-9]*)/", str(link)).group(1))
        num = re.sub(",", "", re.search("\((.*)\)", item.text).group(1))
        
        doc = {
            'from': ff,
            'to': re.search("[^0-9()]*", item.text).group().rstrip(),
            'number_fanfic': int(num)
        }
        
        df.append(doc)
    
    
    
    
df = pd.DataFrame(df)

df.to_csv("crossover_links.csv", index=False)