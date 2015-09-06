import db
import login
import praw
import sys
import util

with open('comment_template.txt') as f:
  comment_template = f.read()

def wrap_comment(text):
  return '>' + '\n>'.join(text.splitlines())
  
def reply(r, comment):
  random_comment = db.random_comment()
  while random_comment['comment_id'] == util.parent(r, comment).id:
    random_comment = db.random_comment()
  thing_id = "t1_" + random_comment['comment_id']
  url = util.parent(r, r.get_info(thing_id=thing_id)).permalink
  text = comment_template.format(wrap_comment(random_comment['text']), url)
  print '[posting] ' + text
  comment.reply(text)

def run():
  no_context = [ '/r/nocontext' ]
  banned_subreddits = [ 'wishlist', 'cringepics', 'askreddit' ]
  r = login.init()
  my_id = login.my_id(r)
  while True:
    try:
      for comment in praw.helpers.comment_stream(r, 'all', verbosity=0):
        subreddit = comment.subreddit.display_name.lower()
        if subreddit in banned_subreddits:
          continue
        text = util.txt(comment).lower().strip()
        if text in no_context \
            and not comment.is_root \
            and not db.has_replied(comment.id):
          db.reply(comment.id)
          login.refresh_praw(r)
          reply(r, comment)
    except praw.errors.OAuthInvalidToken:
      login.refresh_praw(r)

while True:
  try:
    run()
  except:
    print '[posting] ', sys.exc_info()[0]
