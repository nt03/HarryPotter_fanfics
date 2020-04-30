# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 00:18:00 2020

@author: tneha
"""

import sys
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
from datetime import datetime


def get_status(x):
    
    #get the story status: complete/incomplete
    
    if x[-1] == 'Complete':
            status = 'Complete'
            x.pop(-1)
    else:
        status = 'Incomplete'
        
    return status, x


def get_genre(x):
    
    #get the fic genre
    
    if ':' in x[2]:
            return None
    else:
        return x[2]
        
        
 
def get_char(x):
    
    #get the story character list
    
    if ':' in x[-1]:
        return None
    else:
        return x[-1]



def get_date(x, key):   
    
    #convert published/update date to datetime and accomodate for recent fics
    
    try:
        temp = x[key]
        
        #check if the fic was published in the last 24 hrs 
        if re.sub('\d{1,2}', '', temp) == 'h' or re.sub('\d{1,2}', '', temp) == 'm':
            
            #get today's date
            return datetime.now().strftime("%m/%d/%Y")
        
        #else convert it to datetime from string format
        else:
            try:
                return datetime.strptime(temp, '%m/%d/%Y')
            except ValueError:
                temp = temp  + '/' + datetime.now().strftime("%Y")
                return datetime.strptime(temp, '%m/%d/%Y')
                
    except KeyError:
        return None
    
    
def get_story_details(item):
    
    #get fic metadata like author, title, url, synopsis
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
        
    synopsis = item.find("div", class_="z-indent z-padtop").text.replace( item.find("div", class_="z-padtop2 xgray").text, "")
        
    return author, title, synopsis, story_link

        

def clean(item):
    
    '''
    clean the html element to get story metadata
    
    '''
    
    x = item.find("div", class_="z-padtop2 xgray").text.split(" - ")
    
    #get story metadata
    rating = re.sub("Rated: ", "", x[0])    
    lang = x[1]  
    status, x = get_status(x)   
    genre = get_genre(x)
    characters = get_char(x)
    
    
    #edit the remaining list to extract remaining metadata
    if genre is None and characters is None:
            x = x[2:]
    elif genre is None and characters is not None:
        x = x[2:-1]
    elif genre is not None and characters is None:
        x = x[3:]
    else:
        x = x[3:-1]
        
        
    #create a dict of remaining list
    x = [i.split(": ") for i in x]
    x = {key:value for key, value in x}
    
    
    #update date data
    x['Published'] = get_date(x, 'Published')
    x['Updated'] = get_date(x, 'Updated')
    
    
    #get story author, title, synopsis, url
    author, title, synopsis, story_link = get_story_details(item)
    
    
    #create a dict of these attributes      
    doc = {
            'title': title, 
            'author': author, 
            'synopsis':  synopsis, 
            'rating': rating, 
            'language': lang,
            'genre': genre,
            'characters': characters, 
            'status': status,
            'story_link': story_link, 
            
            }
    #merge it with the other dict
    total = {**doc, **x}
    
    return total
    
    
    
    
def main():
    
    #get the page count from commandline
    
    from_page = int(sys.argv[1]) 
    to_page = int(sys.argv[2])
    
    url = "https://www.fanfiction.net/book/Harry-Potter/?&srt=1&r=103&p="
    
    df = []
    
    #loop through the pages
    for i in range(from_page, to_page):
    
        pageurl = url+str(i)
        response = requests.get(pageurl)
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        #extract all story listings on the page
        l = soup.find_all("div", class_="z-list zhover zpointer")
        
        #for each list repeat
        for item in l:
            fic = clean(item)
            df.append(fic)
            
    df = pd.DataFrame(df)
    
    date = datetime.now().strftime("%m.%d.%Y")
    path = "C:/Users/tneha/desktop/ds_self/ffnet/dashboard/"
    
    df.to_csv(f"{path}data/hp_{date}.csv", index= False)
        

    
if __name__ == '__main__':
    main()      
    
    