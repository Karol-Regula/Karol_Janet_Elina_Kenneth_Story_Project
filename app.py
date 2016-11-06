from flask import Flask, render_template, request, session, url_for, redirect, flash
from utils import misc, db

app = Flask(__name__)
app.secret_key = 'KEY'

def isLoggedIn():
  return 'username' in session

@app.route('/')
def default():
  if isLoggedIn():
    return redirect(url_for('stories'))

  return redirect(url_for('auth'))

@app.route('/admin1/')
def createDB():
  db.createDB()
  pointer = db.initializeDB()
  return redirect(url_for('default'))

@app.route('/admin2/')
def initDB():
  pointer = db.initializeDB()
  return redirect(url_for('default'))

@app.route('/auth/')
def auth():
  if isLoggedIn():
    flash('Already logged in!')
    return redirect(url_for('default'))
  return render_template('auth.html')

@app.route('/login/', methods = ['POST'])
def login():
  if 'username' in request.form and 'password' in request.form:
    username = request.form['username']
    password = request.form['password']
    print username, password
    if db.authUser(username, misc.hash(password)):
      session['username'] = username
    else:
      flash('Incorrect username or password!')
  else:
    flash('Please fill out all fields!')

  return redirect(url_for('default'))

@app.route('/register/', methods = ['POST'])
def register():
  if ('username' in request.form and 'password' in request.form):
    username = request.form['username']
    password = request.form['password']
    confirm = request.form['confirm_password']
    print username, password, confirm
    if not db.isRegistered(username):
      if password == confirm:
        db.addUser(username, misc.hash(password))
        session['username'] = username
      else:
        flash('Passwords must match!')
    else:
      flash('Username already in use!')
  else:
    flash('Please fill out all fields!')

  return redirect(url_for('default'))

@app.route('/logout/', methods = ['POST'])
def logout():
  if isLoggedIn():
    session.pop('username')

  return redirect(url_for('default'))

@app.route('/stories/')
def stories():
  if isLoggedIn():
    username = session['username']
    userID = db.getIDOfUser(username)
    return render_template('home.html', user=session['username'], avail_stories=db.getContributedStories(userID), written_stories=db.getContributedStories(userID))

  return redirect(url_for(default))

@app.route('/stories/<storyID>/')
def getStoryID(storyID):
  if isLoggedIn():
    username = session['username']
    userID = db.getIDOfUser(username)
    storyID = int(storyID)
    title = db.getStoryTitle()

    if db.hasContributed(userID, storyID):
      story = db.getStory(storyID)
      return render_template('full_story.html', user=session['username'], title = title, story = story)
    else:
      chapter = db.getLatestChapter(id)
      return render_template('contribute_story.html', user=session['username'], title = title, chapter = chapter)

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
    return render_template('new_story.html', user=session['username'])

  return redirect(url_for('default'))

@app.route('/stories/create/', methods = ['POST'])
def postCreate():
  if isLoggedIn():
    username = session['username']
    userID = db.getIDOfUser(username)

    if 'title' in request.form and 'body' in request.form:
      title = request.form['title']
      body = request.form['body']
      db.createStory(userID, title, body)

  return redirect(url_for('default'))

@app.route('/account/')
def getAccount():
  if isLoggedIn():
    return render_template('account.html', user=session['username'])

  return redirect(url_for('default'))

@app.route('/account/', methods = ['POST'])
def postAccount():
  if isLoggedIn():
    if 'cur_pass' in request.form and 'new_pass' in request.form and 'confirm_pass' in request.form:
      username = session['username']
      curPass = request.form['cur_pass']
      newPass = request.form['new_pass']
      confirmPass = request.form['confirm_pass']

      if db.authUser(username, misc.hash(curPass)):
        if newPass == confirmPass:
          userID = db.getIDOfUser(username)
          db.changePassword(userID, misc.hash(newPass))
          flash('Password changed successfully!')
        else:
          flash('Passwords must match!')
      else:
        flash('Incorrect password!')
    else:
      flash('Please fill out all fields!')

    return render_template('account.html', user=session['username'])
  else:
    return redirect(url_for('default'))

if __name__ == '__main__':
  app.debug = True
  app.run()
