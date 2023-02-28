import spotipy
from spotipy.oauth2 import SpotifyOAuth
from decouple import config
import app

# create a spofy API client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=config("CLIENT_ID"), 
    client_secret=config("CLIENT_SECRET"), 
    redirect_uri=config("REDIRECT_URI"), 
    scope=["user-read-email", "playlist-modify-public"]))

# get uri and id for artists

# taylor_uri = 'spotify:artist:06HL4z0CvFAxyc27GXpf02'

# results = sp.artist_albums(taylor_uri, album_type='album')
# albums = results['items']

# while results['next']:
#     results = sp.next(results)
#     albums.extend(results['items'])

# album_names = []
# for album in albums:
#     if album_names == []:
#         album_names.append(album['name'])
#     elif album['name'] != album_names[-1]:
#         album_names.append(album['name'])

# print(sp)
# for album in album_names:
#     print(album)