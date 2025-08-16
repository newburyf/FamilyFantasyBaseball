import sqlite3

# Python sqlite3 docs
# https://docs.python.org/3/library/sqlite3.html

con = None
cur = None

def setUpConnection():
    global con
    con = sqlite3.connect("db/stats.db")

    global cur
    cur = con.cursor()

def closeConnection():
    global con
    if not con == None:
        con.close()

def initialDBSetup():
    global con
    global cur
    if con == None or cur == None:
        setUpConnection()

    try:
        with open("db/DBSetup.sql", "r") as tables:
            content = tables.read()
            lines = content.split(f"\n\n")

            for l in lines:
                cur.execute(l)

            con.commit()

    except FileNotFoundError:
        print("Could not open the sql file")
    except sqlite3.OperationalError as e:
        print(e)

def addParticipant(name):
    global con
    global cur
    if con == None or cur == None:
        setUpConnection()
    
    cur.execute("INSERT INTO participants (participantName) VALUES (?)", name)
    con.commit()

def addPlayer(first, last):
    global con
    global cur
    if con == None or cur == None:
        setUpConnection()

    cur.execute("INSERT INTO players (firstName, lastName) VALUES (?,?)", first, last)



    