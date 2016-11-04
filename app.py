from flask import Flask, render_template, request, session, url_for, redirect
from utils import misc, db

app = Flask(__name__)
app.secret_key = 'KEY'

def isLoggedIn():
  return 'username' in session

@app.route('/')
def default():
  if isLoggedIn():
    return redirect(url_for('stories'))
  else:
    return redirect(url_for('auth'))

@app.route('/auth/')
def auth():
  if isLoggedIn():
    return redirect(url_for('default'))

  return render_template('auth.html')

@app.route('/login/', methods = ['POST'])
def login():
  if 'username' in request.form and 'password' in request.form:
    username = request.form['username']
    password = request.form['password']
    print username, password

    if db.authUser(username, hash(password)):
      session['username'] = username
      print username + ' logged in'

  return redirect(url_for('default'))

@app.route('/register/', methods = ['POST'])
def register():
  if ('username' in request.form and 'password' in request.form):
    username = request.form['username']
    password = request.form['password']
    confirm = request.form['confirm_password']
    print username, password, confirm
  if not db.isRegistered(username):
    db.addUser( username, hash(password))
    session['username'] = username
    if password == confirm: #and not db.isRegistered(username):
      db.addUser(username, hash(password))
      session['username'] = username
      print username + ' registered'

  return redirect(url_for('default'))

@app.route('/logout/', methods = ['POST'])
def logout():
  if isLoggedIn():
    session.pop('username')

  return redirect(url_for('default'))

@app.route('/stories/')
def stories():
  if isLoggedIn():
    return render_template('home.html', user='NAME', avail_stories='FUNCTION TO PRINT STORIES AVAILABLE', written_stories='FUNCTION TO PRINT THE STORIES WRITTEN IN')

  return redirect(url_for(default))

@app.route('/stories/<storyID>/')
def getStoryID(storyID):
  if isLoggedIn():
    username = session['username']
    userID = db.getIDOfUser(username)
    storyID = int(storyID)

    if db.hasContributed(userID, storyID):
      story = db.getStory(storyID)
      return render_template('full_story.html', story = story)
    else:
      chapter = db.getLatestChapter(id)
      return render_template('contribute_story.html', chapter = chapter)

  return redirect(url_for('default'))

@app.route('/stories/<storyID>/', methods = ['POST'])
def postStoryID(storyID):
  if isLoggedIn():
    username = session['username']
    userID = db.getIDOfUser(username)
    storyID = int(storyID)

    if db.hasContributed(userID, storyID):
      return redirect(url_for('getStoryID'))
    elif 'body' in request.form:
      db.addChapter(storyID, userID, request.form['body'])

  return redirect(url_for('default'))

@app.route('/stories/create/')
def getCreate():
  if isLoggedIn():
    return render_template('new_story.html')

  return redirect(url_for('default'))

@app.route('/stories/create/', methods = ['POST'])
def postCreate():
  if isLoggedIn():
    username = session['username']
    userID = db.getIDOfUser(username)
    storyID = int(storyID)

    if 'title' in request.form and 'body' in request.form:
      title = request.form['title']
      body = request.form['body']
      db.createStory(userID, title, body)

  return redirect(url_for('default'))

if __name__ == '__main__':
  app.debug = True
  app.run()
