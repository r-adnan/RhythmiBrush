import spotipy as spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint

from time import sleep
client_id = "362dc80475a04994834c34e8e9407efa"
client_secret = "e30e2844a83742fd9fd217ae9a8418f7"

scope = "user-read-playback-state, user-modify-playback-state"
sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(client_id="362dc80475a04994834c34e8e9407efa",
                                               client_secret="e30e2844a83742fd9fd217ae9a8418f7",
                                               redirect_uri="http://localhost:8888/callback",
                                               scope='user-read-playback-state,user-modify-playback-state'))
# Shows playing devices
res = sp.devices()
pprint(res)

# Change track
sp.start_playback(uris=['spotify:track:0HUTL8i4y4MiGCPId7M7wb'])
