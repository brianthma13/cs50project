import requests
from bs4 import BeautifulSoup

import time 
from selenium import webdriver 
from selenium.webdriver import Chrome 
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By 
from webdriver_manager.chrome import ChromeDriverManager
import re


def main():

    url = input("Enter url for festival lineup: ")

    if 'coachella' in url:
        artist_list = get_artists_coachella(url)
        print(artist_list)
    elif 'edc' in url:
        artist_list = get_artists_edc(url)
        print(artist_list)
    else:
        print("Please enter a working url.\n")
        main()

def get_artists_coachella(url):
    # leveraged code and process from https://www.zenrows.com/blog/scraping-javascript-rendered-web-pages#installing-the-requirements
    # using selenium to extract javascript rendered webpages (Coachella)
    # initialize headless chrome web driver
        # define options
    options = webdriver.ChromeOptions()
    options.headless = True
    options.page_load_strategy = 'none'

        #return path web driver downloaded
    chrome_path = ChromeDriverManager().install()
    chrome_service = Service(chrome_path)

        # pass defined options and service objects to initialize web driver
    driver = Chrome(options=options, service=chrome_service)
    driver.implicitly_wait(5)
    driver.get(url)
    time.sleep(5)

        # extract content
    artist_elements = driver.find_elements(By.CLASS_NAME, 'title')
    artist_list = []
    [artist_list.append(artist.text) for artist in artist_elements if artist.text not in artist_list]

    artist_list = list(set(artist_list))
    
    return artist_list
        

def get_artists_edc(url):
    r = requests.get(url)
    
    # this function uses BeautifulSoup and Regular Expression to scrape a list of artists off the EDC lineup
    soup = BeautifulSoup(r.content, 'html.parser')
    hrefs = soup.find_all('a', href = "#modal-lineup-artist")

    artist_list = []

    for artist in hrefs:
        temp = artist.get_text()
        suffix = ' (.*)'
        if re.search(suffix, temp) is not None:
            temp = re.sub(suffix, '', temp)
            artist_list.append(temp)
        else:
            artist_list.append(temp)

    return artist_list
      
if __name__ == '__main__':
    main()