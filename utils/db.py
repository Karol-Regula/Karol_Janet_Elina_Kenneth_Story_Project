import sqlite3

#global variables used for database
c = None
db = None

def createDB():
  global c
  initializeDB()
  c.execute('CREATE TABLE users (user_id INTEGER PRIMARY KEY, username TEXT, password TEXT);')
  c.execute('CREATE TABLE chapters (story_id INTEGER, chapter_id INTEGER, user_id INTEGER, title TEXT, body TEXT);')
  closeDB()
  return

def initializeDB():
  global c
  global db
  file = 'data/data.db'
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
  c.execute('INSERT INTO users (username, password) VALUES(\'%s\', \'%s\');' % (username, passhash))
  closeDB()

def createStory(userID, title, body):
  print 'createStory %d %s %s' % (userID, title, body)
  global c
  initializeDB()
  c.execute('SELECT story_id FROM chapters;')
  out = c.fetchall()
  if len(out) == 0:
    storyID = 0
  else:
    out = out[-1]
    storyID = out[0] + 1
  print storyID
  c.execute('INSERT INTO chapters (story_id, chapter_id, user_id, title, body) VALUES(\'%d\', \'%d\', \'%d\', \'%s\', \'%s\');' % (storyID, 0, userID, title, body))
  closeDB()

def addChapter(storyID, userID, body):
  print 'addChapter %d %s %s' % (storyID, userID, body)

def getLatestChapter(storyID):
  print 'getLatestChapter %d' % storyIDs
  return

def getStory(storyID):
  print 'getStory %d' % storyID
  return 'Placeholder Story Content %d' % storyID

def isRegistered(username):
  global c
  initializeDB()
  print 'isRegistered %s' % username
  c.execute('SELECT * FROM users WHERE (username = \'%s\');' % username)
  out = c.fetchall()
  closeDB()
  print out
  print out != []
  return out != []

def getIDOfUser(username):
  print 'getIDOfUser %s' % username
  global c
  initializeDB()
  c.execute('SELECT user_id FROM users WHERE (username = \'%s\');' % username)
  out = c.fetchall()
  out = out[0]#list
  out = out[0]#tuple
  print out
  closeDB()
  return out

def hasContributed(userID, storyID):
  print 'hasContributed %d %d' % (userID, storyID)
  return True

def authUser(username, passhash):
  print 'authUser %s %s' % (username, passhash)
  global c
  initializeDB()
  c.execute('SELECT password FROM users WHERE (username = \'%s\');' % username)
  out = c.fetchall()
  if out == []:
    return False
  out = str(out).split('\'')[1]
  closeDB()
  #print out
  #print passhash
  print out == passhash
  return out == passhash

def changePassword():
  return true

def getStoryTitle():
  return "Placeholder Title"

def getContributedStories(userID):
  print 'getContributedStories'
  global c
  initializeDB()
  c.execute('SELECT title FROM chapters WHERE (user_id = %d);' % userID)
  out = c.fetchall()
  titles = []
  closeDB()
  i = 0
  print out
  while i < len(out):
    print out[i]
    titles.append(str(out[i][0]))
    i += 1
  return titles
