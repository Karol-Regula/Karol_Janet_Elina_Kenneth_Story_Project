import sqlite3


def createDb():
    file = "data/data.db"
    db = sqlite3.connect(file)
    c = db.cursor()

    c.execute("CREATE TABLE users (user_id INTEGER, username TEXT, password INTEGER);")
    #c.execute("INSERT INTO students VALUES(" + k['id'] + ",'" + k['name'] + "'," + k['age'] + ");") #add data to table
    c.execute("CREATE TABLE chapters (story_id INTEGER, chapter_id INTEGER, user_id INTEGER, title TEXT, body TEXT);")

    #To print out values
    #cmd = "SELECT * FROM users"
    #sel = c.execute(cmd)
    #for record in sel:
    #    print record

    db.close()

    '''
    testing protocol:
    $ sqlite3 discobandit.db
    $ .mode column
    $ .header on
    $ SELECT * from students;
    $ SELECT * from courses;
    '''

def initializeDb():
    file = "data/data.db"
    db = sqlite3.connect(file)
    c = db.cursor()
    return c

def insertUser(id, username, password):
    return
