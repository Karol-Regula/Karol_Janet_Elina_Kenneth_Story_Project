import hashlib

def hash(s):
  return hashlib.sha256(s).hexdigest()
