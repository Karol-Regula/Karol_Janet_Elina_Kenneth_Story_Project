import sqlite3

def createDB():
    file = "data/data.db"
    db = sqlite3.connect(file)
    c = db.cursor()

    c.execute("CREATE TABLE users (user_id INTEGER, username TEXT, password INTEGER);")
    c.execute("CREATE TABLE chapters (story_id INTEGER, chapter_id INTEGER, user_id INTEGER, title TEXT, body TEXT);")
    #To print out values
    #cmd = "SELECT * FROM users"
    #sel = c.execute(cmd)
    #for record in sel:
    #    print record
    db.close()

def initializeDB():
    print("Initializing Database")
    file = "data/data.db"
    db = sqlite3.connect(file)
    global c
    c = db.cursor()


def insertUser(id, username, password):
    return

def addUser(username, password):
    createDB()
    print("Initializing Database")
    file = "data/data.db"
    db = sqlite3.connect(file)
    c = db.cursor()
    print("Adding user.")
    c.execute("INSERT INTO students VALUES('" + username + "','" + password + "');")
    db.close()

def isRegistered(username):
    #checks if username already exists
    return False
