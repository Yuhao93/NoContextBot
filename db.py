from pymongo import MongoClient

with open('mongo_login.txt') as f:
  login_url = f.read()
client = MongoClient(login_url)
db = client['no_context_posts']
collection = db['comments']

def insert_if_not_exists(comment_id, text):
  post = {
    "comment_id": comment_id,
    "text": text
  }
  document = collection.find_one({ "comment_id": comment_id })
  if not document is None:
    collection.insert(post)

  





