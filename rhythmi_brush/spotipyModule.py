import spotipy as spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint
import pandas as pd
import time

from time import sleep

clientID = "362dc80475a04994834c34e8e9407efa"
clientSecret = "e30e2844a83742fd9fd217ae9a8418f7"
redirectURI = "http://localhost:8888/callback"
scope='user-read-playback-state,user-modify-playback-state'

class spotipyModule:
    def __init__(self, clientID, clientSecret, redirectURI, scope):
        self.clientID = clientID
        self.clientSecret= clientSecret
        self.redirectURI= redirectURI
        self.scope= scope
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id= self.clientID,
                                               client_secret= self.clientSecret,
                                               redirect_uri= self.redirectURI,
                                               scope= self.scope))

    def getCurrTrack(self):
        return self.sp.current_playback()
    
    def setTrack(self, track_uri='spotify:track:0HUTL8i4y4MiGCPId7M7wb'):
        self.sp.start_playback(uris=[track_uri])
        
    def getStats(self, songURI=None):
        if songURI is None:
            songURI = self.getCurrTrack()['item']['uri']
        
        track_info = self.sp.track(songURI)
        track_features = self.sp.audio_features(songURI)

        acousticness = track_features[0]['acousticness']
        danceability = track_features[0]['danceability']
        energy = track_features[0]['energy']
        liveness = track_features[0]['liveness']
        loudness = track_features[0]['loudness']
        tempo = track_features[0]['tempo']

        track = [acousticness, danceability, energy, liveness, loudness, tempo]

        dy = pd.DataFrame(track).T.values.tolist()
        dy_final = pd.DataFrame(dy, columns=['acousticness', 'danceability', 'energy', 'liveness', 'loudness', 'tempo'])

        return dy_final


def main():
    sp = spotipyModule(clientID, clientSecret, redirectURI, scope)
    currPlayback = sp.getCurrTrack()
    # while True:
    #     currPlayback = sp.getCurrTrack()
    #     min = int((int(currPlayback['progress_ms'])/1000)//60)
    #     seconds = (int(currPlayback['progress_ms'])/1000)%60
    #     print(f'{min}: {seconds:.2f}')
    #     sleep(1)
        
    print(f"Now playing {currPlayback['item']['name']} from {currPlayback['item']['album']['name']} by {currPlayback['item']['album']['artists'][0]['name']}")
    sp.getStats(currPlayback['item']['uri'])
    # pprint(currPlayback.devices())

# Change track
if __name__ == "__main__":
    main()
