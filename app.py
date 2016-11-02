from flask import Flask, render_template, request, session, url_for, redirect
from utils import db

app = Flask(__name__)
app.secret_key = "KEY"
pointer = 0

@app.route("/admin1")
def createdb():
    db.createDb()
    pointer = db.initializeDb()
    return render_template('auth.html')

@app.route("/admin2")
def initdb():
    pointer = db.initializeDb()
    return render_template('auth.html')

@app.route("/")
def login():
    return render_template('auth.html')

#@app.route("/auth")

#@app.route("/login")

#@app.route("/register")

#@app.route("/logout")

#@app.route("/stories")

if __name__ == '__main__':
    app.debug = True
    app.run()
