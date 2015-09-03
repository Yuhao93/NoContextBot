def txt(comment):
  return ''.join(comment.body).encode('utf-8')

def parent(r, comment):
  return r.get_info(thing_id=comment.parent_id)
