# 1. import libraries
import requests # to download html code
from bs4 import BeautifulSoup # to navigate through the html code
import pandas as pd
import numpy as np
import re

def scrape_hot100():
    '''
    This function scraps the 100 best songs with respective artists from the website hot-100
    
    output -> A df with top 100 songs and artists
    '''
       
    url = "https://www.billboard.com/charts/hot-100/"

    # Error handling
    response = requests.get(url)
    if (response.status_code != 200):
        print("Wrong response: ", response.status_code)
        return 0
    
    soup = BeautifulSoup(response.text, 'html.parser')

    # Song selector ----------------------------------------    
    song_selector = '''
    #post-1479786 > div.pmc-paywall > 
    div > div > div > div > div > ul > 
    li.lrv-u-width-100p > ul > li > h3
    '''
    song_list = soup.select(song_selector)
    song_list = [text.get_text().replace('\n',"").replace('\t',"") for text in song_list]
    
    # Artist selector ---------------------------------------
    artist_selector = '''
    #post-1479786 > div.pmc-paywall > 
    div > div > div > div > div > ul > 
    li.lrv-u-width-100p > ul > li > span
    '''
    artist_list = soup.select(artist_selector)
    artist_list = [text.get_text().replace('\n',"").replace('\t',"") for text in artist_list]
    new_list = []
    for i in range(len(artist_list)):
        if (i % 4 == 0):
            new_list.append(artist_list[i])
    artist_list = new_list

    
    # Create the df ----------------------------------------    
    best_100 = pd.DataFrame({'songs':song_list,'artists':artist_list})
    
    # Save as CSV ------------------------------------------    
    best_100.to_csv('best_100.csv')
    
    return best_100