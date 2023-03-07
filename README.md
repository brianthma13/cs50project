# Festy
### VIDEO DEMO: https://youtu.be/FXqU90prtcQ
### DESCRIPTION:

Festy is an app I designed that can pull a list of performing artist from festival lineups online, or takes a user's custom artist list and generates a Spotify playlist for the user, leveraging Spotify's API.

Festy has a Python and Flask backend and the frontend is HTML, CSS, with a little bit of JavaScript.

## Frontend Files
### Package: static/
#### festy.png
- This is the festy logo image used on the main page

### Package: templates/
#### cover.css
- This css file constain css globals for the bootstrap template used for the app frontend.
#### error.html
- This file extends "layout.html" and provides an error message and form to go back to the "/" route which renders "index.html".
#### index.html
- Index.html provides two forms, one to select from a list of festivals, the other allows a user to enter a list of their own artists.
  - Festivals Form: Originally, I was going to have this be a URL-typed input field requesting the user input a lineup URL of their preferred festival (i.e.: <a href="coachella.com/lineup">coachella.com/lineup</a> and <a href="lasvegas.electricdaisycarnival.com/lineup">lasvegas.electricdaisycarnival.com/lineup</a>. Because the code of Festy only focuses on Coachella and EDC Las Vegas, I decided to change it to a dropdown containing just the festivals Festy can pull a list of artists from, which allows for less errors to occur. The input button "Make me a playlist!" submits the user's input and triggers a popup that notifies the user that the playlist generating process might take a few minutes.
  - Custom List Form: This form uses a field area for the user to put in a list of comma-separated artists for Festy to make a playlist of. This also includes an input button "Make me a playlist!" that submits the user's input and triggers a popup that notifies the user that the playlist generating process might take a few minutes.
#### layout.html
- Layout.html is the primary html file for the web app. This file also includes css styling and html code from bootstrap, to make the interface look nice. 
#### success.html
- Success.html displays how the lenght of time it took to make a playlist, and a list of artists that were not found on Spotify. The Go Back button triggers the action for the app to go to the primary route.

### .gitignore and .env
- I have a gitignore file which calls out certain files to not be tracked by git. In this case, I have a **.env** file that includes environment variables specific to my Spotify account: "CLIENT_ID" and "CLIENT_SECRET" which are needed to access Spotify's API via OAuth.
- For this reason, .env is not included

### app.py
app.py is the backbone of Festy. This file contains the routes and functions that enable Festy to pull lists from websties and make calls to the Spotify API.
Modules: This section lists out all the modules used in app.py
- flask, requests, beautifulsoup, time, selenium, random, datetime, jinja, spotipy, decouple
- BeautifulSoup and Selenium are used to web scrape the festival lineup pages to get a list of artist names.
- Spotipy is a lightweight python library for the Spotify API
Below the modules, the environment is setup, and the global variable FESTIVALS is established.
@app.route("/")
- renders the index.html page
@app.route("/generate")
- This route provides the logic for the app to generate playlists.
- In this route, I start a timer to display how long each process takes and creates a Spotify API object using Spotipy and the .env variables
- A variable for the user's specific ID is pulled for later use
- A series of "if" statements determine where to pull the lists and which functions are executed for webscraping.
  - If the festivals form was used, it will see if Festy will execute the "get_artists_coachella()" or "get_artists_edc()" function. I have a 3rd option for future expansion to include Tomorrowland.
  - If the custom list form was used, it turns the user's input into a list
- get_artists_id()
  - This function uses artist_list and calls the "search" endpoint to search for each artist in the list on Spotify's database to get the artist's ID from the JSON result. This function also assumes that the first artist listed (most popular) is the intended artist, as well as makes a list of artists not found.
  - Due to the limitations of this API, Festy is not able to do batch searches when using the artist names to find their Spotify ID, so there is an API request and response for each artist that unfortunately takes a while and slows down the process.
  - Returns: artist_ids, not_found
- get_track_list()
  - This function uses if statements to combine a list of artist top tracks
  - If the festival form was used, it will pull the track ID of a random song from the artist's top songs
  - If the custom list form was used, it will pull the IDs of all the artist's top songs. Assuming this list is considerable shorter than the festival lineups.
  - Returns: track_list
- make_playlist()
  - This function creates a blank playlist on the user's Spotify library and get the ID of the new playlist
  - Returns: playlist_id
- add_songs()
  - This function calls the "add items to playlist" endpoint; splits artist lists into lists of 100, if the original list is longer; and adds the tracks in batches to the new playlist
- This route renders the "success.html" layout when complete
