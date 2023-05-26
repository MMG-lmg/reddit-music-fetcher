import requests
import requests.auth
import json

def login(client_id,client_secret,reddit_username,reddit_password):
    client_auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    post_data = {"grant_type": "password", "username": reddit_username, "password": reddit_password}
    headers = {"user-agent": "music-fetcher by u/ludikonj35"}
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
    if response.status_code == requests.codes.ok :
        try :
            data = response.json()
        except requests.exceptions.JSONDecodeError:
            print("Response json conversion error 204: No content or malformed JSON")
        if 'access_token' in data: return data['access_token']
        else: return 'error'
    else: return 'error'
        