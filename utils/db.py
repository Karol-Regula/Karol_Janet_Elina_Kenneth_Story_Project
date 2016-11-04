import sqlite3

def createDB():
  file = "data/data.db"
  db = sqlite3.connect(file)
  c = db.cursor()

  c.execute("CREATE TABLE users (user_id INTEGER, username TEXT, password INTEGER);")
  #c.execute("INSERT INTO students VALUES(" + k['id'] + ",'" + k['name'] + "'," + k['age'] + ");") #add data to table
  c.execute("CREATE TABLE chapters (story_id INTEGER, chapter_id INTEGER, user_id INTEGER, title TEXT, body TEXT);")

  #To print out values
  #cmd = "SELECT * FROM users"
  #sel = c.execute(cmd)
  #for record in sel:
  #    print record

  db.close()

  '''
  testing protocol:
  $ sqlite3 discobandit.db
  $ .mode column
  $ .header on
  $ SELECT * from students;
  $ SELECT * from courses;
  '''

def initializeDB():
  file = "data/data.db"
  db = sqlite3.connect(file)
  c = db.cursor()
  return c

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


