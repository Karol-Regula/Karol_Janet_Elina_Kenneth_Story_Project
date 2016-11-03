from flask import Flask, render_template, request, session, url_for, redirect
from utils import misc, db

app = Flask(__name__)
app.secret_key = 'KEY'
pointer = 0

def isLoggedIn():
  return 'username' in session

@app.route('/')
def default():
  if isLoggedIn():
    return redirect(url_for('stories'))

  return redirect(url_for('auth'))

@app.route("/admin1")
def createDB():
  db.createDB()
  pointer = db.initializeDB()
  return render_template('auth.html')

@app.route("/admin2")
def initDB():
  pointer = db.initializeDB()
  return render_template('auth.html')

@app.route('/auth')
def auth():
  if isLoggedIn():
    return redirect(url_for('default'))
    
  return render_template('auth.html')

@app.route('/login', methods = ['POST'])
def login():
  if 'username' in request.form and 'password' in request.form:
    username = request.form['username']
    password = request.form['password']

    if db.authUser(username, hash(password)):
      session['username'] = username

  return redirect(url_for('default'))

@app.route('/register', methods = ['POST'])
def register():
  if 'username' in request.form and 'password' in request.form:
    username = request.form['username']
    password = request.form['password']
    confirm = request.form['confirm_password']

    if password == confirm and not db.isRegistered(username):
      db.addUser(username, hash(password))
      session['username'] = username

  return redirect(url_for('default'))

@app.route('/logout', methods = ['POST'])
def logout():
  if isLoggedIn():
    session.pop('username')

  return redirect(url_for('default'))

@app.route('/stories')
def stories():
  if isLoggedIn():
    return render_template('home.html', user='user')

  return redirect(url_for(default))

@app.route('/stories/<storyID>')
def getStoryID(storyID):
  if isLoggedIn():
    userID = db.getIDOfUser(username)

    if db.hasContributed(userID, storyID):
      story = db.getStory(storyID)
      return render_template('full_story.html', story = story)
    else:
      chapter = db.getLatestChapter(id)
      return render_template('contribute_story.html', chapter = chapter)

  return redirect(url_for('default'))
  
@app.route('/stories/<storyID>', methods = ['POST'])
def postStoryID(storyID):
  if isLoggedIn():
    userID = db.getIDOfUser(username)

    if db.hasContributed(userID, storyID):
      return redirect(url_for('getStoryID'))
    else if 'body' in request.form:
      db.addChapter(storyID, userID, request.form['body'])

  return redirect(url_for('default'))

@app.route('/stories/create')
def getCreate():
  if isLoggedIn():
    return render_template('new_story.html')
    
  return redirect(url_for('default'))      
  
@app.route('/stories/create', methods = ['POST'])
def postCreate():
  if isLoggedIn():
    userID = db.getIDOfUser(username)

    if 'title' in request.form and 'body' in request.form:
      title = request.form['title']
      body = request.form['body']
      db.createStory(userID, title, body)
      
  return redirect(url_for('default'))      

if __name__ == '__main__':
  app.debug = True
  app.run()
