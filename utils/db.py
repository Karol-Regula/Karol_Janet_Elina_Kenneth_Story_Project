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

def initializeDB():
  global c, db
  file = 'data/data.db'
  db = sqlite3.connect(file)
  c = db.cursor()

def closeDB():
  global db
  db.commit()
  db.close()

def addUser(username, passhash):
  initializeDB()
  c.execute('INSERT INTO users (username, password) VALUES(\'%s\', \'%s\');' % (username, passhash))
  closeDB()

def createStory(userID, title, body):
  initializeDB()
  c.execute('SELECT story_id FROM chapters;')
  out = c.fetchall()

  if out:
    storyID = 0
  else:
    storyID = out[-1][0] + 1

  c.execute('INSERT INTO chapters (story_id, chapter_id, user_id, title, body) VALUES(\'%d\', \'%d\', \'%d\', \'%s\', \'%s\');' % (storyID, 0, userID, title, body))
  closeDB()

def addChapter(storyID, userID, title, body):
  initializeDB()
  c.execute('SELECT chapter_id FROM chapters WHERE(story_id = \'%d\');' % storyID)
  out = c.fetchall()
  lastChapter = out[-1][0]
  c.execute('INSERT INTO chapters (story_id, chapter_id, user_id, title, body) VALUES(\'%d\', \'%d\', \'%d\', \'%s\', \'%s\');' % (storyID, lastChapter + 1, userID, title, body))
  closeDB()

def getLatestChapter(storyID):
  initializeDB()
  c.execute('SELECT body FROM chapters WHERE (story_id = \'%s\');' % storyID)
  out = c.fetchall()
  closeDB()
  return out[-1][0]

def getStory(storyID):
  initializeDB()
  c.execute('SELECT body FROM chapters WHERE (story_id = \'%s\');' % storyID)
  out = c.fetchall()
  closeDB()

  story = []

  for i in range(len(out)):
    story.append(out[i][0])

  return story

def isRegistered(username):
  initializeDB()
  c.execute('SELECT * FROM users WHERE (username = \'%s\');' % username)
  out = c.fetchall()
  closeDB()
  return bool(out)

def getIDOfUser(username):
  initializeDB()
  c.execute('SELECT user_id FROM users WHERE (username = \'%s\');' % username)
  out = c.fetchall()
  closeDB()

  return out[0][0]

def hasContributed(userID, storyID):
  initializeDB()
  c.execute('SELECT user_id FROM chapters WHERE (story_id = \'%d\');' % storyID)
  out = c.fetchall()
  closeDB()

  for i in range(len(out)):
    if out[i][0] == userID:
      return True

  return False

def authUser(username, passhash):
  initializeDB()
  c.execute('SELECT password FROM users WHERE (username = \'%s\');' % username)
  out = c.fetchall()
  closeDB()

  if not out:
    return False

  return out[0][0] == passhash

def changePassword(userID, passhash):
  initializeDB()
  c.execute('UPDATE users SET password = \'%s\' WHERE (user_id = %d);' % (passhash, userID))
  closeDB()

def getStoryTitle(storyID):
  initializeDB()
  c.execute('SELECT title FROM chapters WHERE (story_id = \'%s\');' % storyID)
  out = c.fetchall()
  closeDB()
  return out[0][0]

def getContributedStories(userID):
  initializeDB()
  c.execute('SELECT title, story_id FROM chapters WHERE (user_id = %d);' % userID)
  out = c.fetchall()
  closeDB()

  titles = []

  for i in range(len(out)):
    titles.append([out[i][0], out[i][1]])

  return titles

def getNotContributedStories(userID):
  initializeDB()
  c.execute('SELECT title, story_id FROM chapters WHERE (user_id != %d);' % userID)
  out = c.fetchall()
  closeDB()

  titles = []

  for i in range(len(out)):
    append = True
    title = out[i][0]
    storyID = out[i][1]
    current = titles.append([title, storyID])

    if not hasContributed(userID, storyID):
      if current not in titles:
        titles.append(current)

  return titles
