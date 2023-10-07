import requests
from urllib.parse import urlencode
import base64
import webbrowser
from flask import Flask, request, redirect
import os
from requests import post
import json
import time 
from pprint import pprint 

client_id = "362dc80475a04994834c34e8e9407efa"
client_secret = "e30e2844a83742fd9fd217ae9a8418f7"

gct_url = 'https://api.spotify.com/v1/me/player/currently-playing'

auth_headers = {
    "client_id": client_id,
    "response_type": "code",
    "redirect_uri": "http://localhost:7777/callback",
    "scope": "user-library-read"
}

webbrowser.open("https://accounts.spotify.com/authorize?" + urlencode(auth_headers))

app = Flask(__name__)

@app.route('/callback')
def callback():
    return "Spotify Authorized"

if __name__ == "__main__":
    app.run(port=7777)


def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]

    return token

token = get_token()
# print(token)

def get_current_track(access_token):
    response = requests.get(gct_url, headers = {
        "Authorization":f"Bearer {access_token}"
    })
    json_resp = response.json()

    track_id = json_resp['item']['id']
    track_name = json_resp['item']['name']
    artists = [artist for artist in json_resp['item']['artists']]

    link = json_resp['item']['external_urls']['spotify']
    
    artist_names = ', '.join([artist['name'] for artist in artists])

    current_track_info = {
        "id": track_id,
        "track_name": track_name,
        "artists": artist_names
        "link": link
    }

    return current_track_info

def main():
    current_track_id = None
    
    while True:
        current_track_info = get_current_track(token)

        if current_track_info['id'] != current_track_id:
            pprint(
                current_track_info,
                indent=4
            )
            current_track_id = current_track_info['id']
        
        time.sleep(1)

main()