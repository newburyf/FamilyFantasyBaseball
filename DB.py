import sqlite3
from Enums import HitterStats as HS, PitcherStats as PS

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
    
    cur.execute("INSERT INTO participants (participantName) VALUES (?);", name)
    con.commit()

def addPlayer(mlbID, first, last):
    global con
    global cur
    if con == None or cur == None:
        setUpConnection()

    cur.execute("INSERT INTO players (mlbID, firstName, lastName) VALUES (?,?,?);", [mlbID, first, last])
    con.commit()

def addDraft(mlbID, participant, position, teamID, roundNum, year):
    global con
    global cur
    if con == None or cur == None:
        setUpConnection()

    cur.execute("""
                    INSERT INTO draft 
                    (playerID, participantName, positionCode, teamID, draftRoundNum, year) 
                    VALUES (?,?,?,?,?);""",
                    [mlbID, participant, position, teamID, roundNum, year])
    
    con.commit()

def addGame(teamOne, teamTwo, round, date):
    global con
    global cur
    if con == None or cur == None:
        setUpConnection()

    cur.execute("INSERT INTO games (teamOne, teamTwo, round, date) VALUES (?,?,?,?);", teamOne, teamTwo, round, date)
    con.commit()

def addGameStats(playerID, gameID, hitterStats, pitcherStats, points):
    global con
    global cur
    if con == None or cur == None:
        setUpConnection()

    cur.execute("""
                    INSERT INTO gameStats
                    (playerID, gameID, hTB, hRBI, hR, hSB, hBB, hK, pIP, pW, pL, pHD, pSV, pER, pH, pK, pBB, points)
                    VALUES (?,?,?, ?,?,?, ?,?,?, ?,?,?, ?,?,?, ?,?,?)
                ;""", [playerID, gameID, hitterStats[HS.TB.value], hitterStats[HS.RBI.value], hitterStats[HS.R.value], hitterStats[HS.SB.value], hitterStats[HS.BB.value], hitterStats[HS.K.value], pitcherStats[PS.IP.value], pitcherStats[PS.W.value], pitcherStats[PS.L.value], pitcherStats[PS.HD.value], pitcherStats[PS.SV.value], pitcherStats[PS.ER.value], pitcherStats[PS.H.value], pitcherStats[PS.K.value], pitcherStats[PS.BB.value], points])
    con.commit()

def getTeam(teamID):
    global con
    global cur
    if con == None or cur == None:
        setUpConnection()
    
    res = cur.execute("SELECT location, teamName FROM teams WHERE mlbID = ?;", [teamID])
    location, team = res.fetchone()
    return location + " " + team
        