import db
import login
import praw

with open('comment_template.txt') as f:
  comment_template = f.read()

def reply(comment):
  random_comment = db.random_comment()
  new_comment = comment.reply(comment_template.format(random_comment.text,
      random_comment.comment_id))
  db.insert_if_not_exists(new_comment.id, new_comment.text)

def run():
  no_context = [ 'r/nocontext', '/r/nocontext' ]
  r = login.init()
  my_id = login.my_id(r)
  while True:
    login.refresh_praw(r)
    for comment in r.get_comments('all'):
      text = ''.join(comment.body).encode('utf-8').lower().strip()
      if not comment.is_root
          and text in no_context
          and not db.exists(comment.id)
          and not comment.author.id == my_id:
        reply(comment)

run()
