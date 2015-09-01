import db
import login
import praw

with open('comment_template.txt') as f:
  comment_template = f.read()

def reply(comment):
  random_comment = db.random_comment()
  text = comment_template.format(random_comment.text,
      random_comment.comment_id)
  print '[posting] ' + text
  new_comment = comment.reply(text)
  db.insert_if_not_exists(new_comment.id, new_comment.text)

def run():
  no_context = [ '/r/nocontext' ]
  r = login.init()
  my_id = login.my_id(r)
  for comment in praw.helpers.comment_stream(r, 'all', verbosity=0):
    text = ''.join(comment.body).encode('utf-8').lower().strip()
    if not comment.is_root
        and text in no_context
        and not db.exists(comment.id)
        and not comment.author.id == my_id:
      login.refresh_praw(r)
      reply(comment)
run()
