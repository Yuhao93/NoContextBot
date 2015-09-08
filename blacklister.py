import db
import login
import praw
import sys
import time

def run():
  last_seen_message = None
  seen = []
  r = login.init()
  while True:
    try:
      newest_message = None
      for message in r.get_messages(place_holder=last_seen_message):
        author = message.author
        if newest_message == None:
          newest_message = message.id
          last_seen_message = newest_message
        if message.subject == 'blacklist' and not author.id in seen:
          print '[blacklist] ' + author.id
          db.blacklist_user(author.id)
          seen.append(author.id)
      time.sleep(60)
    except praw.errors.OAuthInvalidToken:
      login.refresh_praw(r)

while True:
  try:
    run()
  except:
    print '[blacklister] ', sys.exc_info()[0]
