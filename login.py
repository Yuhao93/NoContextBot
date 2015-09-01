import json
import praw
import requests
import requests.auth

user_agent = "I make comments with no context!"
with open('credentials/client.json') as f:
  client_json = json.load(f)
  client_id = client_json['client-id']
  client_secret = client_json['secret']

def get_access_token():
  client_auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
  with open('credentials/login.json') as login:
    post_data = json.load(login)
  headers = { "User-Agent": user_agent }
  response = requests.post("https://www.reddit.com/api/v1/access_token", 
      auth=client_auth, data=post_data, headers=headers)
  response_obj = response.json()
  return response_obj['access_token']  

def init():
  r = praw.Reddit(user_agent)
  r.set_oauth_app_info(
      client_id=client_id,
      client_secret=client_secret,
      redirect_uri='http://example.com/unused/redirect/uri')
  refresh_praw(r)
  return r

def refresh_praw(praw_instance):
  praw_instance.set_access_credentials(set(["submit"]), get_access_token())


