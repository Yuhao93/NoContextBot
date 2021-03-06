import json
import random
import time
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
blacklist = db['blacklist']
banned = db['banned']

def insert_if_not_exists(comment_id, text):
  if not exists(comment_id):
    collection.insert_one({
      "comment_id": comment_id,
      "text": text
    })

def reply(comment_id):
  replies.insert_one({
    "comment_id": comment_id,
    "timestamp": int(round(time.time() * 1000))
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

def is_blacklisted(user_id):
  return not blacklist.find_one({
    "user_id": user_id
  }) is None

def blacklist_user(user_id):
  if not is_blacklisted(user_id):
    blacklist.insert_one({
      "user_id": user_id
    })

def is_banned(subreddit_id):
  return not banned.find_one({
    "subreddit_id": subreddit_id
  }) is None

def ban_subreddit(subreddit_id):
  if not is_banned(subreddit_id):
    banned.insert_one({
      "subreddit_id": subreddit_id
    })
