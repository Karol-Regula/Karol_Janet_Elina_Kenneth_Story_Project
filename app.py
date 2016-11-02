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

@app.route('/auth')
def auth():
  if isLoggedIn():
    return redirect(url_for('default'))
  else:
    return render_template('auth.html')

@app.route('/login', methods = ['POST'])
def login():
  if 'username' in request.form and 'password' in request.form:
    username = request.form['username']
    password = request.form['password']

    if authUser(username, hash(password)):
      session['username'] = username

  return redirect(url_for('default'))

# @app.route('/register')

# @app.route('/logout')

# @app.route('/stories')

if __name__ == '__main__':
  app.debug = True
  app.run()
