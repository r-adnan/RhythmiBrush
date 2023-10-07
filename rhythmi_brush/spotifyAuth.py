import requests
from urllib.parse import urlencode
import base64
import webbrowser

client_id = "362dc80475a04994834c34e8e9407efa"
client_secret = "e30e2844a83742fd9fd217ae9a8418f7"

auth_headers = {
    "client_id": client_id,
    "response_type": "code",
    "redirect_uri": "http://localhost:7777/callback",
    "scope": "user-library-read"
}

webbrowser.open("https://accounts.spotify.com/authorize?" + urlencode(auth_headers))


# code = "362dc80475a04994834c34e8e9407efa"

# encoded_credentials = base64.b64encode(client_id.encode() + b':' + client_secret.encode()).decode("utf-8")

# token_headers = {
#     "Authorization": "Basic" + encoded_credentials,
#     "Content-Type": "application/x-www-form-urlencoded"
# }

# token_data = {
#     "grant_type": "authorization_code",
#     "code": code,
#     "redirect_uri": "http://localhost:7777/callback"
# }

# r = requests.post("https://accounts.spotify.com/api/token", data=token_data, headers=token_headers)

# token = r.json()["access_token"]

# print(token)
