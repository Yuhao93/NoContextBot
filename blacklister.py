import db
import login
import praw
import sys
import time
import traceback
import re

def run():
  ban_template = 'you\'ve been banned from (/r/.+)'
  last_seen_message = None
  r = login.init()
  while True:
    try:
      newest_message = None
      for message in r.get_messages(place_holder=last_seen_message):
        author = message.author
        match_res = re.match(ban_template, message.subject)
        if newest_message == None:
          newest_message = message.id
          last_seen_message = newest_message
        if message.subject == 'blacklist':
          print '[blacklist] user:' + author.id
          db.blacklist_user(author.id)
        elif not match_res is None:
          subreddit = match_res.group(1).lower()
          print '[blacklist] subreddit' + subreddit
          db.ban_subreddit(subreddit)
      time.sleep(60)
    except praw.errors.OAuthInvalidToken:
      login.refresh_praw(r)

while True:
  try:
    run()
  except:
    traceback.print_exc()
