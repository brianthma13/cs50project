from flask import Flask, render_template, request, redirect

import requests
from bs4 import BeautifulSoup
import time 
from selenium import webdriver 
from selenium.webdriver import Chrome 
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By 
from webdriver_manager.chrome import ChromeDriverManager
import re
import random
import datetime
from selenium.webdriver.support.ui import Select

# API 
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from decouple import config

from jinja2 import Environment, PackageLoader, select_autoescape
env = Environment(
    loader=PackageLoader("app"),
    autoescape=select_autoescape()
)

app = Flask(__name__)

FESTIVALS = [
    'Coachella',
    'EDC Las Vegas'
]

@app.route("/")
@app.route('/index')
def index():
    return render_template("index.html", festivals = FESTIVALS)

@app.route("/generate", methods=['POST'])
def main():

    year = datetime.date.today().year

    # t_start = time.time()

    # create a spofy API client
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=config("CLIENT_ID"), 
        client_secret=config("CLIENT_SECRET"), 
        redirect_uri=config("REDIRECT_URI"), 
        scope=["user-read-email", "playlist-modify-public"]
        ))

    # gets spotify user id
    user_id = sp.me()['id']

    # x = input("Which festival do you want a playlist for? (COACHELLA, or EDCLV): ").lower()

    x = request.form.get("festival")
    if x not in FESTIVALS:
            return render_template("error.html", message="Invalid festival")

    if x == 'Coachella':
        playlist_name = "Coachella " + str(year) + " Playlist"
        url = "https://coachella.com/lineup"
        artist_list = get_artists_coachella(url)
    elif x == 'EDC Las Vegas':
        playlist_name = "EDC LV " + str(year) + " Playlist"    
        url = "https://lasvegas.electricdaisycarnival.com/lineup"
        artist_list = get_artists_edc(url)
    elif x == 'Tomorrowland':
        playlist_name = "Tomorrowland " + str(year) + " Playlist"
        url = "https://www.tomorrowland.com/en/festival/line-up/stages/"
        artist_list = get_artists_tml(url)
    

    # return list of artist ids
    artist_ids = get_artists_id(artist_list, sp)

    track_list = get_track_list(artist_ids, sp)

    playlist_id = make_playlist(user_id, sp, playlist_name)

    add_songs(playlist_id,track_list, user_id, sp)

    # t_end = time.time()
    # t = t_end - t_start

    # print(f"{playlist_name} created")
    # print(f"This process took {t:.2} seconds")
    return render_template("success.html", x = x)

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
    active_tab = soup.find('div', "tabs__content tabs__content--active")

    artists = active_tab.find_all('a')
    
    artist_list = []

    for artist in artists:
        temp = artist.attrs['data-artist-name']
        artist_list.append(temp)

    # list to set to list to get rid of dupes
    artist_set = set(artist_list)
    artist_list = list(artist_set)

    return artist_list

def get_artists_tml(url):
    url = url
    # proposed tomorrowland lineup playlist
    return

def get_artists_id(l, sp):
    # this function retreives artist spotify id 
    # this function assumes that each artist listed is the most popular one (first on list)

    artist_ids = []

    for artist in l:
        results = sp.search(q = 'artist: ' + artist, type = 'artist')
        if results['artists']['items'][0]['name'].lower().replace(" ", "") == artist.lower().replace(" ", ""):
            artist_id = results['artists']['items'][0]['id']
            artist_ids.append(artist_id)
    return artist_ids

def get_track_list(artist_ids, sp):
    # this function randomly retreives the URI for one of the top 5 tracks of an artist
    track_list = []
    
    for id in artist_ids:
        top_tracks = sp.artist_top_tracks('spotify:artist:' + id)
        x = len(top_tracks['tracks'])
        if x > 0:
            rand = random.randint(0,x-1)
            rand_track = top_tracks['tracks'][rand]['uri']
            track_list.append(rand_track)
        else:
            pass

    return track_list
    
def make_playlist(uid, sp, plname):

    # creates playlist for user
    playlist = sp.user_playlist_create(user = uid, name= plname)
    playlist_id = playlist['id']

    return playlist_id

def add_songs(plid, tl, uid, sp):
    # this function adds track from track list tl to playlist with id pl
    print(len(tl))
    def group_it(tl):
        # this function splits tl into groups of 100 tracks
        for i in range(0, len(tl), 100):
            yield tl[i:i + 100]
    tl = list(group_it(tl))
    
    for l in tl:
        sp.user_playlist_add_tracks(uid, plid, l)
    
    return
    
if __name__ == '__main__':
    main()