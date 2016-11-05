import hashlib

def sanitize(s):

  return s

def desanitize(s):

  return s

def hash(s):
  return hashlib.sha256(s).hexdigest()
