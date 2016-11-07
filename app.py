from flask import Flask, render_template, request, session, url_for, redirect, flash
from utils import misc, db

app = Flask(__name__)
app.secret_key = 'KEY'

def isLoggedIn():
  if 'username' in session:
    if db.isRegistered(session['username']):
      return True

    session.pop('username')

  return False

@app.route('/')
def default():
  if isLoggedIn():
    return redirect(url_for('stories'))

  return redirect(url_for('auth'))

@app.route('/admin/')
def createDB():
  db.createDB()
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
    avail_stories = db.getNotContributedStories(userID)
    written_stories = db.getContributedStories(userID)
    
    return render_template('home.html',
                           user = username,
                           avail_stories = avail_stories,
                           written_stories = written_stories)

  return redirect(url_for('default'))

@app.route('/stories/<storyID>/')
def getStoryID(storyID):
  if isLoggedIn():
    username = session['username']
    userID = db.getIDOfUser(username)
    storyID = int(storyID)
    title = db.getStoryTitle(storyID)

    if db.hasContributed(userID, storyID):
      story = db.getStory(storyID)
      return render_template('full_story.html',
                             user = username,
                             title = title,
                             story = story)
    else:
      chapter = db.getLatestChapter(storyID)
      return render_template('contribute_story.html',
                             user = username,
                             title = title,
                             chapter = chapter,
                             storyID = storyID)

  return redirect(url_for('default'))

@app.route('/stories/<storyID>/', methods = ['POST'])
def postStoryID(storyID):
  if isLoggedIn():
    username = session['username']
    userID = db.getIDOfUser(username)
    storyID = int(storyID)
    title = db.getStoryTitle(storyID)

    if db.hasContributed(userID, storyID):
      return redirect(url_for('getStoryID'))
    elif 'body' in request.form:
      db.addChapter(storyID, userID, title, request.form['body'])

  return redirect(url_for('default'))

@app.route('/stories/create/')
def getCreate():
  if isLoggedIn():
    return render_template('new_story.html', user = session['username'])

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
    return render_template('account.html', user = session['username'])

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

    return render_template('account.html', user = username)
  else:
    return redirect(url_for('default'))

if __name__ == '__main__':
  app.debug = True
  app.run()
