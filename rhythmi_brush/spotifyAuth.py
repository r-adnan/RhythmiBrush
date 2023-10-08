import base64
import datetime
from urllib.parse import urlencode

import requests
import json

from urllib.parse import urlencode
import webbrowser
from flask import Flask, request, redirect
import os
from requests import post

client_id = "362dc80475a04994834c34e8e9407efa"
client_secret = "e30e2844a83742fd9fd217ae9a8418f7"

gct_url = 'https://api.spotify.com/v1/me/player/currently-playing'

auth_headers = {
    "client_id": client_id,
    "response_type": "code",
    "redirect_uri": "http://localhost:7777/callback",
    "scope": "user-read-playback-state"
}

webbrowser.open("https://accounts.spotify.com/authorize?" + urlencode(auth_headers))

app = Flask(__name__)

@app.route('/callback')
def callback():
    return "Spotify Authorized. You can close out of this page."

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


class SpotifyAPI(object):
    client_id = None
    client_secret = None
    access_token = token 

    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret

    def base_search(self, query_params): # type
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/search"
        lookup_url = f"{endpoint}?{query_params}"
        r = requests.get(lookup_url, headers=headers)
        if r.status_code not in range(200, 299):  
            return {}

        json_object = json.dumps(r.json(), indent=4)
        with open('search_results.txt', 'w') as f:
            f.write(json_object)
        return r.json()
    
    def search(self, query=None, operator=None, operator_query=None, search_type='artist' ):
        if query == None:
            raise Exception("A query is required")
        if isinstance(query, dict):
            query = " ".join([f"{k}:{v}" for k,v in query.items()])
        if operator != None and operator_query != None:
            if operator.lower() == "or" or operator.lower() == "not":
                operator = operator.upper()
                if isinstance(operator_query, str):
                    query = f"{query} {operator} {operator_query}"
        query_params = urlencode({"q": query, "type": search_type.lower()})
        print(query_params)
        return self.base_search(query_params)

    def get_current_track(self):
        response = requests.get(gct_url, headers = {
            "Authorization":f"Bearer {self.access_token}"
        })
        json_resp = response.json()

        # track_id = json_resp['item']['id']
        # track_name = json_resp['item']['name']
        # artists = [artist for artist in json_resp['item']['artists']]

        # link = json_resp['item']['external_urls']['spotify']
        
        json_object = json.dumps(json_resp, indent=4)
        with open('search_results.txt', 'w') as f:
            f.write(json_object)

        # artist_names = ', '.join([artist['name'] for artist in artists])

        # current_track_info = {
        #     "id": track_id,
        #     "track_name": track_name,
        #     "artists": artist_names,
        #     "link": link
        # }

        return 

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

spotify = SpotifyAPI("362dc80475a04994834c34e8e9407efa", "e30e2844a83742fd9fd217ae9a8418f7")
spotify.get_current_track()