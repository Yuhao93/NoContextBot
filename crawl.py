import db
import login
import praw
import requests
import requests.auth

def run():
  no_context = [ 'r/nocontext', '/r/nocontext' ]
  r = login.init()
  while True:
    login.refresh_praw(r)
    for comment in r.get_comments('all'):
      text = ''.join(comment.body).encode('utf-8').lower().strip()
      if not comment.is_root and text in no_context:
        parent = r.get_info(thing_id=comment.parent_id)
        parent_text = ''.join(parent.body).encode('utf-8')
        db.insert_if_not_exists(parent.id, parent_text)

run()
