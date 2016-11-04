import sqlite3

#global variables used for database
c = None
db = None

def createDB():
  global c
  initializeDB()
  c.execute("CREATE TABLE users (user_id INTEGER PRIMARY KEY, username TEXT, password TEXT);")
  c.execute("CREATE TABLE chapters (story_id INTEGER, chapter_id INTEGER, user_id INTEGER, title TEXT, body TEXT);")
  closeDB()
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
  initializeDB()
  print 'addUser %s %s' % (username, passhash)
  c.execute("INSERT INTO users (username, password) VALUES('" + username + "','" + passhash + "');")
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
  global c
  global db
  initializeDB()
  print 'isRegistered %s' % username
  c.execute("SELECT * FROM users WHERE (username = '" + username + "');")
  out = c.fetchall()
  closeDB()
  print out
  print out != []
  return out != []

def getIDOfUser(username):
  print 'getIDOfUser %s' % username
  return 0

def hasContributed(userID, storyID):
  print 'hasContributed %d %d' % (userID, storyID)
  return True

def authUser(username, passhash):
  print 'authUser %s %s' % (username, passhash)
  global c
  global db
  initializeDB()
  c.execute("SELECT password FROM users WHERE (username = '" + username + "');")
  out = c.fetchall()
  if out == []:
    return False
  out = str(out).split('\'')[1]
  closeDB()
  #print out
  #print passhash
  print out == passhash
  return out == passhash
