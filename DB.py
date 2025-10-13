import sqlite3
from Enums import HitterStats as HS, PitcherStats as PS

con = None
cur = None

def setUpConnection():
    global con
    con = sqlite3.connect("db/stats.db")

    global cur
    cur = con.cursor()

def closeConnection():
    global cur
    if not cur == None:
        cur.close()

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

def checkParticipantExists(name, year):
    global con
    global cur
    if con == None or cur == None:
        setUpConnection()
    
    res = cur.execute("SELECT * FROM participants WHERE participantName = ? AND year = ?;", [name, year])
    return res.fetchone() is not None

def addParticipant(name, year):
    global con
    global cur
    if con == None or cur == None:
        setUpConnection()
    
    added = False
    if not checkParticipantExists(name, year):
        cur.execute("INSERT INTO participants (participantName, year) VALUES (?,?);", [name, year])
        con.commit()
        added = True

    return added

def getAllParticipants(year):
    global con
    global cur
    if con == None or cur == None:
        setUpConnection()

    res = cur.execute("SELECT participantID, participantName FROM participants WHERE year = ?;", [year])
    return res.fetchall()

def checkPlayerExists(mlbID):
    global con
    global cur
    if con == None or cur == None:
        setUpConnection()

    res = cur.execute("SELECT * FROM players WHERE mlbID = ?;", [mlbID])
    return res.fetchone() is not None

def addPlayer(mlbID, first, last):
    global con
    global cur
    if con == None or cur == None:
        setUpConnection()

    added = False
    if not checkPlayerExists(mlbID):    
        cur.execute("INSERT INTO players (mlbID, firstName, lastName) VALUES (?,?,?);", [mlbID, first, last])
        con.commit()
        added = True
    
    return added

def getAllPlayers():
    global con
    global cur
    if con == None or cur == None:
        setUpConnection()

    res = cur.execute("SELECT * FROM players;")
    playerInfo = []
    for mlbID, firstName, lastName in res.fetchall():
        playerInfo.append( ( mlbID, firstName + " " + lastName ) )

    return playerInfo

def checkDraftExists(participantID, playerID, year, roundNum):
    global con
    global cur
    if con == None or cur == None:
        setUpConnection()
    
    res = cur.execute("SELECT * FROM draft WHERE playerID = ? AND participantID = ? AND year = ? AND draftRoundNum = ?;", [playerID, participantID, year, roundNum])
    return res.fetchone() is not None

def addDraft(mlbID, participant, position, teamID, roundNum, year):
    global con
    global cur
    if con == None or cur == None:
        setUpConnection()

    added = False
    if not checkDraftExists(participant, mlbID, year, roundNum):

        cur.execute("""
                    INSERT INTO draft 
                    (playerID, participantID, positionCode, teamID, draftRoundNum, year) 
                    VALUES (?,?,?,?,?,?);""",
                    [mlbID, participant, position, teamID, roundNum, year])
        con.commit()
        added = True

    return added

def getCurrentDraft(year, round):
    global con
    global cur
    if con == None or cur == None:
        setUpConnection()

    res = cur.execute("""SELECT participantID, playerID, teamID, positionCode 
                         FROM draft 
                         WHERE year = ? AND draftRoundNum = ?;""", 
                         (year, round))
    return res.fetchall()    

def getCurrentDraftWithNames(year, round):
    global con
    global cur
    if con == None or cur == None:
        setUpConnection()

    res = cur.execute("""SELECT draft.participantID, draft.playerID, players.lastName, teams.code, draft.positionCode 
                         FROM draft 
                         INNER JOIN players ON draft.playerID = players.mlbID
                         INNER JOIN teams ON draft.teamID = teams.mlbID
                         WHERE draft.draftRoundNum = ? AND draft.year = ?;""",
                         [round, year])
    return res.fetchall()

def getDraftedPlayerByRound(year, round, participant, pos):
    global con
    global cur
    if con == None or cur == None:
        setUpConnection()

    res = cur.execute("""SELECT draft.playerID, players.firstName, players.lastName, draft.teamID, teams.code
                         FROM draft
                         INNER JOIN players ON draft.playerID = players.mlbID
                         INNER JOIN teams on draft.teamID = teams.mlbID
                         WHERE draft.year = ? AND draft.draftRoundNum = ? AND draft.participantID = ? AND draft.positionCode = ?;""",
                         [year, round, participant, pos])
    return res.fetchone()

def checkGameExists(mlbID):
    global con
    global cur
    if con == None or cur == None:
        setUpConnection()

    res = cur.execute("SELECT * FROM games WHERE mlbID = ?;", [mlbID])
    return res.fetchone() is not None

def addGame(mlbID, homeTeam, awayTeam, roundCode, date):
    global con
    global cur
    if con == None or cur == None:
        setUpConnection()

    if not checkGameExists(mlbID):
        cur.execute("INSERT INTO games (mlbID, homeTeam, awayTeam, roundCode, date) VALUES (?,?,?,?,?);", [mlbID, homeTeam, awayTeam, roundCode, date])
        con.commit()

def addGameStats(playerID, gameID, hitterStats, pitcherStats, points):
    global con
    global cur
    if con == None or cur == None:
        setUpConnection()

    cur.execute("""
                    INSERT INTO gameStats
                    (playerID, gameID, hTB, hRBI, hR, hSB, hBB, hK, pO, pW, pL, pHD, pSV, pER, pH, pK, pBB, points)
                    VALUES (?,?,?, ?,?,?, ?,?,?, ?,?,?, ?,?,?, ?,?,?)
                ;""", [playerID, gameID, hitterStats[HS.TB.value], hitterStats[HS.RBI.value], hitterStats[HS.R.value], hitterStats[HS.SB.value], hitterStats[HS.BB.value], hitterStats[HS.K.value], pitcherStats[PS.O.value], pitcherStats[PS.W.value], pitcherStats[PS.L.value], pitcherStats[PS.HD.value], pitcherStats[PS.SV.value], pitcherStats[PS.ER.value], pitcherStats[PS.H.value], pitcherStats[PS.K.value], pitcherStats[PS.BB.value], points])
    con.commit()

def getGameStatsForRound(year, roundCode):
    global con
    global cur
    if con == None or cur == None:
        setUpConnection()
    
    res = cur.execute("""
                         SELECT gameStats.playerID, gameStats.points, games.date
                         FROM games INNER JOIN gameStats on games.mlbID = gameStats.gameID
                         WHERE games.roundCode = ? AND strftime('%Y', games.date) = ?
                         ORDER BY games.date;
                      """, [roundCode, str(year)])
    
    return res.fetchall()

def getTeam(teamID):
    global con
    global cur
    if con == None or cur == None:
        setUpConnection()
    
    res = cur.execute("SELECT location, teamName FROM teams WHERE mlbID = ?;", [teamID])
    location, team = res.fetchone()
    return location + " " + team

def getAllTeams():
    global con
    global cur
    if con == None or cur == None:
        setUpConnection()

    res = cur.execute("SELECT mlbID, location, teamName FROM teams;")
    teamInfo = []
    for mlbID, location, teamName in res.fetchall():
        teamInfo.append( ( mlbID, location + " " + teamName ) )
    return teamInfo

def getAllPositions():
    global con
    global cur
    if con == None or cur == None:
        setUpConnection()

    res = cur.execute("SELECT * FROM positions;")
    return res.fetchall()

def getAllRounds():
    global con
    global cur
    if con == None or cur == None:
        setUpConnection()

    res = cur.execute("SELECT number, name FROM rounds;")
    return res.fetchall()

def generateJSONData(year):
    data = {
        "year": year,
        "participants": generateJSONParticipants(year),
        "rounds": generateJSONRounds(year),
    }

    return data

def generateJSONParticipants(year):
    allParticipants = getAllParticipants(year)

    formattedParticipants = []
    for p in allParticipants:
        formattedP = { 
            "id": p[0], 
            "name": p[1],
        }
        formattedParticipants.append(formattedP)
    
    return formattedParticipants

def generateJSONRounds(year):
    allRounds = getAllRounds()
    allParticipants = getAllParticipants(year)
    formattedRounds = []

    for round in allRounds:
        roundDraft = getCurrentDraftWithNames(year, round[0])

        if len(roundDraft) > 0:
            # doing draft results
            formattedDraft = []
            
            for participant in allParticipants:
                participantDraft = []
                for draftee in roundDraft:
                    if int(draftee[0]) == participant[0]:
                        formattedDraftee = {
                            "playerID": draftee[1],
                            "playerLast": draftee[2],
                            "teamCode": draftee[3],
                            "positionCode": draftee[4],
                        }

                        participantDraft.append(formattedDraftee)

                formattedParticipant = {
                    "participantID": participant[0],
                    "draftees": participantDraft,
                }
                formattedDraft.append(formattedParticipant)

            # getting scores
            formattedScores = []
            roundScores = getGameStatsForRound(year, round[0])

            currentDate = "0000-00-00"
            currentDateScores = []
            for score in roundScores:
                if score[2] != currentDate:
                    if len(currentDateScores) > 0:
                        formattedDay = {
                            "date": currentDate,
                            "scores": currentDateScores.copy(),
                        }
                        formattedScores.append(formattedDay)
                        currentDateScores.clear()
                    
                    currentDate = score[2]
                
                formattedScore = {
                    "playerID": score[0],
                    "points": score[1],
                }
                currentDateScores.append(formattedScore)

            # appending the last day's scores
            if len(currentDateScores) > 0:
                formattedDay = {
                    "date": currentDate,
                    "scores": currentDateScores.copy(),
                }
                formattedScores.append(formattedDay)

            formattedRound = {
                "name": round[1],
                "draftees": formattedDraft,
                "scores": formattedScores,
            }
            formattedRounds.append(formattedRound)

    return formattedRounds