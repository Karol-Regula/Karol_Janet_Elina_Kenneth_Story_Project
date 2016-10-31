from flask import Flask, render_template, request, session, url_for, redirect

app = Flask(__name__)
app.secret_key = "KEY"

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
