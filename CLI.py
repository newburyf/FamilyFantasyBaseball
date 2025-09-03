import DB as db
import statsapi
from Enums import HitterStats as HS, HitterPoints as HP, PitcherStats as PS, PitcherPoints as PP
import json

def printCommands():
    commands = [
        "STATS (Update stats)",
        "PUSH (Push stats changes)",
        "PLAYER (Add player to database)",
        "DRAFT (Add player draft to database)",
        "PARTICIPANT (Add participant to database)",
        "SETUP (Do initial database setup)",
        "EXIT",
    ]
    print(f"\nCommands:")
    for i, c in enumerate(commands):
        print(f"{i + 1}: {c}")

def updateStats():
    print(f"Updating stats\n--------------")
    dateString = input("Enter the date (YYYY-MM-DD) to update stats for (0 to cancel): ")
    year = dateString.split("-")[0] 
    
    if dateString != "0":
        print(f"\nRounds:")
        allRounds = db.getAllRounds()
        i = 1
        for r in allRounds:
            print(f"{i}. {r[1]}")
            i += 1

        selectedRound = input("Enter the number of the round of the date (0 to cancel): ")
        roundNum = 0
        try:
            roundNum = int(selectedRound)
        except:
            print("Please enter a valid round number")

        if roundNum != 0:
            roundCode = allRounds[roundNum - 1][0]

            currentPlayers = db.getCurrentDraft(year, roundCode)
            for player in currentPlayers:
                teamID = player[2]
                games = statsapi.schedule(team=teamID, date=dateString)
                if len(games) != 0:
                    gameID = games[0]["game_id"]
                    boxscoreData = statsapi.boxscore_data(gameID)

                    side = "home"
                    awayID = boxscoreData["teamInfo"]["away"]["id"]
                    if awayID == teamID:
                        side = "away"
                    
                    homeID = boxscoreData["teamInfo"]["home"]["id"]
                    db.addGame(gameID, homeID, awayID, roundCode, dateString)

                    hitterStats = [0 for i in range(0, len(HS))]
                    pitcherStats = [0 for i in range(0, len(PS))]
                    points = 0

                    playerID = player[1]
                    positionCode = player[3]
                    
                    if positionCode == "IF" or positionCode == "OF":
                        for playerStats in boxscoreData[side + "Batters"]:
                            if playerStats["personId"] == playerID:
                                hitterStats[HS.RBI.value] = int(playerStats["rbi"])
                                hitterStats[HS.R.value] = int(playerStats["r"])
                                hitterStats[HS.SB.value] = int(playerStats["sb"])
                                hitterStats[HS.BB.value] = int(playerStats["bb"])
                                hitterStats[HS.K.value] = int(playerStats["k"])

                                hits = int(playerStats["h"])
                                tb = 0

                                doubles = int(playerStats["doubles"])
                                tb += 2 * doubles
                                hits -= doubles

                                triples = int(playerStats["triples"])
                                tb += 3 * triples
                                hits -= triples

                                hr = int(playerStats["hr"])
                                tb += 4 * hr
                                hits -= hr

                                tb += hits # singles

                                hitterStats[HS.TB.value] = tb

                                for i in range(0, len(hitterStats)):
                                    points += HP[i] * hitterStats[i]

                                break
                        
                        else:
                            for playerStats in boxscoreData[side + "Pitchers"]:
                                if playerStats["personId"] == playerID:
                                    o = 0
                                    ip = playerStats["ip"]
                                    full, partial = ip.split(".")
                                    o = int(full) * 3 + int(partial)
                                    pitcherStats[PS.O.value] = o

                                    w = 0
                                    if "W" in playerStats["note"]:
                                        w = 1
                                    pitcherStats[PS.W.value] = w

                                    l = 0
                                    if "L" in playerStats["note"]:
                                        l = 1
                                    pitcherStats[PS.L.value] = l

                                    hd = 0
                                    if "H" in playerStats["note"]:
                                        hd = 1
                                    pitcherStats[PS.HD.value] = hd

                                    sv = 0
                                    if "S" in playerStats["note"]:
                                        sv = 1
                                    pitcherStats[PS.SV.value] = sv

                                    pitcherStats[PS.ER.value] = int(playerStats["er"])
                                    pitcherStats[PS.H.value] = int(playerStats["h"])
                                    pitcherStats[PS.K.value] = int(playerStats["k"])
                                    pitcherStats[PS.BB.value] = int(playerStats["bb"])
                                    
                                    for i in range(0, len(pitcherStats)):
                                        points += PP[i] * pitcherStats[i]

                                    break
                        
                    db.addGameStats(playerID, gameID, hitterStats, pitcherStats, points)

            print("Stats updated")
        else:
            print("Canceling")
    else:
        print("Canceling")

    return True

def pushStatsChanges():
    currentYearString = input("Enter the current year (0 to cancel): ")
    currentYear = 0
    try:
        currentYear = int(currentYearString)
    except:
        print("Please enter a valid year")

    if currentYear != 0:
        scoresData = db.generateJSONData(currentYear)
        with open(f"website/data/{currentYear}.json", "w") as f:
            json.dump(scoresData, f)

        print("Stats changes pushed")
    
    return True

def addPlayer():
    print(f"Adding player\n-------------")
    playerName = input("Enter the last name of the player you want to add (0 to cancel): ")
    currentYearString = input("Enter the current year (0 to cancel): ")
    currentYear = 0
    try:
        currentYear = int(currentYearString)
    except:
        print("Please enter a valid year")

    if playerName != "0" and currentYear != 0:
        players = statsapi.lookup_player(playerName, season=currentYear)
        if len(players) == 0:
            print("Could not find any players with that last name")
        else:
            print("Players:")
            i = 1
            for p in players:
                team = db.getTeam(int(p['currentTeam']['id']))
                print(f"{i}. {p['fullName']}, {team}")
                i += 1

            userInput = input("Please enter the number of the player to add them to the database (0 to cancel): ")
            playerNum = 0

            try:
                playerNum = int(userInput)
            except:
                print("Please enter a valid player number")

            if playerNum != 0:
                toAdd = players[playerNum-1]
                added = db.addPlayer(toAdd['id'], toAdd['firstName'], toAdd['lastName'])
                if added:
                    print(f"Added {players[playerNum-1]['fullName']} to the database")
                else:
                    print("Player is already in the database")
            else:
                print("Canceling")
    else:
        print("Canceling")

    return True

def addDraft():
    print(f"Adding draft result\n-------------------")
    yearString = input("Enter the current year (0 to cancel): ")
    year = 0
    try:
        year = int(yearString)
    except:
        print("Please enter a valid year")

    if year != 0:
        print(f"\nParticipants:")
        allParticipants = db.getAllParticipants(year)
        if len(allParticipants) == 0:
            print(f"No participants registered for {yearString} yet")
        else:
            i = 1
            for p in allParticipants:
                print(f"{i}. {p[1]}")
                i += 1
        
            selectedParticipant = input("Please enter the number of the participant that drafted a player (0 to cancel): ")
            participantNum = 0

            try:
                participantNum = int(selectedParticipant)
            except:
                print("Please enter a valid participant number")

            if participantNum != 0:
                participantID = allParticipants[participantNum - 1][0]

                allPlayers = db.getAllPlayers()
                print(f"\nPlayers:")
                i = 1
                for p in allPlayers:
                    print(f"{i}. {p[1]}")
                    i += 1

                selectedPlayer = input("Please enter the number of the player being drafted (0 to cancel): ")
                playerNum = 0

                try:
                    playerNum = int(selectedPlayer)
                except:
                    print("Please enter a valid player number")

                if playerNum != 0:
                    playerID = allPlayers[playerNum-1][0]
                    
                    allTeams = db.getAllTeams()
                    print(f"\nTeams:")
                    i = 1
                    for t in allTeams:
                        print(f"{i}. {t[1]}")
                        i += 1

                    selectedTeam = input("Please enter the number of the team the player is currently on (0 to cancel): ")
                    teamNum = 0
                    try:
                        teamNum = int(selectedTeam)
                    except:
                        print("Please enter a valid team number")
                    
                    if teamNum != 0:
                        teamID = allTeams[teamNum - 1][0]

                        allPositions = db.getAllPositions()
                        print(f"\fPositions:")
                        i = 1
                        for p in allPositions:
                            print(f"{i}. {p[1]}")
                            i += 1

                        selectedPosition = input("Please enter the number of the position the player is being drafted at (0 to cancel): ")
                        positionNum = 0
                        try:
                            positionNum = int(selectedPosition)
                        except:
                            print("Please neter a vaild position number")
                        
                        if positionNum != 0:
                            positionCode = allPositions[positionNum - 1][0]

                            allRounds = db.getAllRounds()
                            print(f"\nRounds:")
                            i = 1
                            for r in allRounds:
                                print(f"{i}. {r[1]}")
                                i += 1

                            selectedRound = input("Please enter the current round (0 to cancel): ")
                            roundNum = 0
                            try:
                                roundNum = int(selectedRound)
                            except:
                                print("Please enter a valid round number")

                            if roundNum != 0:
                                roundCode = allRounds[roundNum - 1][0]

                                added = db.addDraft(playerID, participantID, positionCode, teamID, roundCode, year)
                                if added:
                                    print("Draft result added")
                                else:
                                    print("Draft result already exists")
                            else:
                                print("Canceling")
                        else:
                            print("Canceling")
                    else:
                        print("Canceling")
                else:
                    print("Canceling")
            else:
                print("Canceling")

    return True

def addParticipant():
    print("Adding participant")
    name = input("Enter the name of the participant you want to add (0 to cancel): ")
    yearString = input("Enter the curret year (0 to cancel): ")
    year = 0
    try:
        year = int(yearString)
    except:
        print("Please enter a valid year")

    if name != "0" and year != 0:
        added = db.addParticipant(name, year)
        if added:
            print(f"\"{name}\" added as a participant for {yearString}")
        else:
            print("Participant already exists")
    else:
        print("Canceling")

    return True

def initialDBSetUp():
    print(f"Doing initial database setup\nTHIS WILL WIPE YOUR EXISTING DATABASE IF YOU HAVE ONE SET UP ALREADY!")
    userConfirmation = input("Enter y/n to do setup/cancel: ")

    if userConfirmation == "y":
        print("Setting up database")
        db.initialDBSetup()
        print("Set up finished")
    else:
        print("Canceling setup")

    return True
    
def main():
    print(f"Welcome to Family Fantasy Baseball!\n-----------------------------------")

    commands = [
        updateStats,
        pushStatsChanges,
        addPlayer,
        addDraft,
        addParticipant,
        initialDBSetUp,
        exit
    ]
    
    running = True
    while running:
        printCommands()
        userCommand = input("Please enter the number of the command you wish to run: ")
        print()
        
        commandNum = 0
        try:
            commandNum = int(userCommand)

        except Exception as e:
            print(e)
            print("Please enter a valid command number.")
        
        commandToRun = commands[commandNum - 1]
        running = commandToRun()

if __name__ == "__main__":
    main()