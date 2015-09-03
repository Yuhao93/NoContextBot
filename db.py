import json
import random
from pymongo import MongoClient

with open('credentials/mongo.json') as f:
  json_login = json.load(f)
  username = json_login['username']
  password = json_login['password']
  url = json_login['url']
  port = json_login['port']
  db_name = json_login['db']

client = MongoClient(url, port)
db = client[db_name]
db.authenticate(username, password)
collection = db['comments']
replies = db['replies']

def insert_if_not_exists(comment_id, text):
  if not exists(comment_id):
    collection.insert_one({
      "comment_id": comment_id,
      "text": text
    })

def reply(comment_id):
  replies.insert_one({
    "comment_id": comment_id  
  })

def has_replied(comment_id):
  return not replies.find_one({
    "comment_id": comment_id
  }) is None

def exists(comment_id):
  return not collection.find_one({ "comment_id": comment_id }) is None

def random_comment():
  cnt = collection.count()
  randomNumber = random.randint(0, cnt - 1)
  return collection.find().limit(-1).skip(randomNumber).next()



