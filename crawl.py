import db
import login
import praw

def run():
  no_context = [ 'r/nocontext', '/r/nocontext' ]
  r = login.init()
  my_id = login.my_id(r)
  while True:
    login.refresh_praw(r)
    for comment in r.get_comments('all'):
      text = ''.join(comment.body).encode('utf-8').lower().strip()
      if not comment.is_root and text in no_context:
        parent = r.get_info(thing_id=comment.parent_id)
        if parent.author.id == my_id:
          continue
        parent_text = ''.join(parent.body).encode('utf-8')
        print '[adding] ' + parent_text
        db.insert_if_not_exists(parent.id, parent_text)

run()
