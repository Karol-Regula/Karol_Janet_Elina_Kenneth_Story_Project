import sqlite3

#global variables used for database
c = None
db = None

def createDB():
  c.execute("CREATE TABLE users (user_id INTEGER PRIMARY KEY, username TEXT, password TEXT);")
  c.execute("CREATE TABLE chapters (story_id INTEGER, chapter_id INTEGER, user_id INTEGER, title TEXT, body TEXT);")
  return

def initializeDB():
  global c
  global db
  file = "data/data.db"
  db = sqlite3.connect(file)
  c = db.cursor()
  return c

def closeDB():
  global db
  db.commit()
  db.close()

def addUser(username, passhash):
  global c
  global db
  initializeDB()
  print 'addUser %s %s' % (username, passhash)
  c.execute("INSERT INTO users (username, password) VALUES('" + username + "','" + passhash + "');")
  #c.execute("INSERT INTO users VALUES " + (1 + ", b, c);")
  closeDB()

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
  #checks if username already exists
  print 'isRegistered %s' % username
  return False

def getIDOfUser(username):
  print 'getIDOfUser %s' % username
  return 0

def hasContributed(userID, storyID):
  print 'hasContributed %d %d' % (userID, storyID)
  return True

def authUser(username, passhash):
  print 'authUser %s %s' % (username, passhash)
  return True
