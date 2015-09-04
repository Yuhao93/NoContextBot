import db
import login
import praw
import sys
import util

def run():
  no_context = [ '/r/nocontext' ]
  r = login.init()
  my_id = login.my_id(r)
  while True:
    try:
      for comment in praw.helpers.comment_stream(r, 'all', verbosity=0):
        text = util.txt(comment).lower().strip()
        if not comment.is_root and text in no_context:
          parent = util.parent(r, comment)
          if parent.author.id == my_id:
            continue
          parent_text = ''.join(parent.body).encode('utf-8')
          print '[adding] ' + parent_text
          db.insert_if_not_exists(parent.id, parent_text)
    except praw.errors.OAuthInvalidToken:
      login.refresh_praw(r) 

while True:
  try:
    run()
  except:
    print '[crawler] ', sys.exec_info()[0]
