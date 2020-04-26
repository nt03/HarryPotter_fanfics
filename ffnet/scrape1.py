# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 19:54:40 2019

@author: tneha

Code to scrape harry potter fanfiction data from first 30000 pages from fanfiction.net using requests 
Wrangle and structure it using BeautifulSoup and regex libraries

output: pandas dataframe and a CSV
 
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup
import re


url = "https://www.fanfiction.net/book/Harry-Potter/?&srt=1&r=103&p="


df=[]

num_pages = 30000

#loop through first 30000 pages
for i in range(1, num_pages):
    
    pageurl = url+str(i)
    response = requests.get(pageurl)
    
    soup = BeautifulSoup(response.text, "html.parser")
    

    #extract all story listings 
    l = soup.find_all("div", class_="z-list zhover zpointer")
    
    #for each list repeat
    for item in l:
     
        x = item.find("div", class_="z-padtop2 xgray").text.split(" - ")
        
        rating = re.sub("Rated: ", "", x[0])
        lang = x[1]
        
        #check status
        if x[-1] == 'Complete':
            status = 'Complete'
            x.pop(-1)
        else:
            status = None
            
        
        #check genre and characters
        if ':' in x[2]:
            genre = None
        else:
            genre = x[2]
            
        if ':' in x[-1]:
            characters = None
        else:
            characters = x[-1]
            
        if genre is None and characters is None:
            x = x[2:]
        elif genre is None and characters is not None:
            x = x[2:-1]
        elif genre is not None and characters is None:
            x = x[3:]
        else:
            x = x[3:-1]
        
        #create a dict of remaining
        x = [i.split(":") for i in x]
        x = {key:value for key, value in x}
        
        #get synopsis text
        synopsis = item.find("div", class_="z-indent z-padtop").text.replace( item.find("div", class_="z-padtop2 xgray").text, "")
        
        
        #get the link, author and title using 'a' tags
        n = item.find_all('a')
        
        if len(n) == 2:
            story_link = "https://www.fanfiction.net" + n[0]['href']
            title = n[0].text
            author = n[1].text
        elif len(n) == 3:
            story_link = "https://www.fanfiction.net" + n[0]['href']
            title = n[0].text
            author = n[2].text
        else:
            story_link = "https://www.fanfiction.net" + n[0]['href']
            title = n[0].text
            author = None
            
         
        #create a dict of these attributes      
        doc = {
                'story_link': story_link, 
                'title': title, 
                'author': author, 
                'synopsis':  synopsis, 
                'rating': rating, 
                'language': lang,
                'genre': genre,
                'characters': characters
                
                }
        #merge it with the other dict
        total = {**doc, **x}
        
        #append to the list
        df.append(total)
    
df = pd.DataFrame(df)    

df.to_csv("data/hp.csv", index= False)