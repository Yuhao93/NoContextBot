import db
import login
import praw
import sys
import traceback
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
  context_comment = r.get_info(thing_id=thing_id)
  parent_comment = util.parent(r, context_comment)
  url = parent_comment.permalink
  nsfw = ""
  if context_comment.submission.over_18:
    nsfw = " [NSFW]"
  text = comment_template.format(wrap_comment(random_comment['text']), nsfw, \
      url)
  print '[posting] ' + text
  comment.reply(text)

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
          if not parent.author.id == my_id:
            parent_text = ''.join(parent.body).encode('utf-8')
            print '[adding] ' + parent_text
            db.insert_if_not_exists(parent.id, parent_text)
        
        subreddit = comment.subreddit.display_name.lower()
        if db.is_banned(subreddit):
          continue
        if text in no_context \
            and not comment.is_root \
            and not db.has_replied(comment.id) \
            and not db.is_blacklisted(comment.author.id):
          db.reply(comment.id)
          login.refresh_praw(r)
          reply(r, comment)

    except praw.errors.OAuthInvalidToken:
      login.refresh_praw(r) 

while True:
  try:
    run()
  except:
    traceback.print_exc()
