import sqlite3

file = "data/data.db"
db = sqlite3.connect(file)
c = db.cursor()

def createDB():
  c.execute("CREATE TABLE users (user_id INTEGER, username TEXT, password INTEGER);")
  c.execute("CREATE TABLE chapters (story_id INTEGER, chapter_id INTEGER, user_id INTEGER, title TEXT, body TEXT);")
  return

def initializeDB():
  file = "data/data.db"
  db = sqlite3.connect(file)
  c = db.cursor()
  return c

def addUser(username, password):
  print("Adding user.")
  c.execute("INSERT INTO students VALUES('" + username + "','" + password + "');")

def isRegistered(username):
  #checks if username already exists
  return False

def createStory(userID, title, body):
  print 'createStory %d %s %s' % (userID, title, body)

def addChapter(storyID, userID, body):
  print 'addChapter %d %s %s' % (storyID, userID, body)

def getLatestChapter(storyID):
  print 'getLatestChapter %d' % storyID
  return 'testChapter %d' % storyID

def getStory(storyID):
  print 'getStory %d' % storyID
  return 'testStory %d' % storyID

def isRegistered(username):
  print 'isRegistered %s' % username
  return False

def getIDOfUser(username):
  print 'getIDOfUser %s' % username
  return 0

def hasContributed(userID, storyID):
  print 'hasContributed %d %d' % (userID, storyID)
  return True

def addUser(username, passhash):
  print 'addUser %s %s' % (username, passhash)

def authUser(username, passhash):
  print 'authUser %s %s' % (username, passhash)
  return True
