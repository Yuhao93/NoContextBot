import json
from pymongo import MongoClient

with open('credentials/mongo.json') as f:
  json_login = json.load(f)
  username = json_login['username']
  password = json_login['password']
  url = json_login['url']
  port = json_login['port']
  db = json_login['db']

client = MongoClient(url, port)
db = client[db]
db.authenticate(username, password)
collection = db['comments']

def insert_if_not_exists(comment_id, text):
  post = {
    "comment_id": comment_id,
    "text": text
  }
  document = collection.find_one({ "comment_id": comment_id })
  if not document is None:
    collection.insert(post)

  





