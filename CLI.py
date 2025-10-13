import DB as db
import statsapi
from Enums import HitterStats as HS, HitterPoints as HP, PitcherStats as PS, PitcherPoints as PP
import json

# utility input methods
def getNumberInputFromList(message, list):
    print(message)
    for i, item in enumerate(list):
        print(f"{i + 1}. {item}")

    listSelection = input("Enter the number of the item to select (0 to cancel): ")
    listNum = -1

    while listNum == -1:
        try:
            listNum = int(listSelection)

            if(listNum > len(list) or listNum < 0):
                listNum = -1
                raise ValueError
            
        except ValueError:
            listSelection = input("Please enter a valid number: ")
    print()
    return listNum

def getNumberInput(numType, min, max):
    numString = input(f"Enter a {numType} (between {min} and {max}, inclusive) (0 to cancel): ")
    num = -1

    while num == -1:
        try:
            num = int(numString)

            if (num < min and num != 0) or num > max:
                num = -1
                raise ValueError
            
        except ValueError:
            numString = input("Please enter a valid number: ")
    print()
    return num

def getDateInput(dateType):
    dateString = input(f"Enter the date for {dateType} (MM-DD) (0 to cancel): ")

    validDate = False
    while not validDate and dateString != "0":

        try:
            parts = dateString.split("-")
            if len(parts) != 2:
                raise ValueError
            
            if len(parts[0]) != 2:
                raise ValueError
            
            month = int(parts[0])
            if month < 1 or month > 12:
                raise ValueError
            
            if len(parts[1]) != 2:
                raise ValueError
            
            day = int(parts[1])
            # only validating days for months that playoff games happen for now, verifying all months is a pain
            if day < 1 or (month == 9 and day > 30) or (month == 10 and day > 31) or (month == 11 and day > 30):
                raise ValueError

            validDate = True

        except ValueError:
                dateString = input("Please enter a valid date (MM-DD): ")

    print()
    return dateString

# command methods
def updateStats(year):
    print(f"Updating stats\n--------------")
    date = getDateInput("stats update")
    fullDate = f"{year}-{date}"
    if date != 0:
        allRounds = db.getAllRounds()
        round = getNumberInputFromList("Rounds:", [r[1] for r in allRounds])
        if round != 0:
            roundCode = allRounds[round - 1][0]
            currentPlayers = db.getCurrentDraft(year, roundCode)
            for player in currentPlayers:
                teamID = player[2]
                games = statsapi.schedule(team=teamID, date=fullDate)
                if len(games) != 0:
                    gameID = games[0]["game_id"]
                    boxscoreData = statsapi.boxscore_data(gameID)

                    side = "home"
                    awayID = boxscoreData["teamInfo"]["away"]["id"]
                    if awayID == teamID:
                        side = "away"
                    
                    homeID = boxscoreData["teamInfo"]["home"]["id"]
                    db.addGame(gameID, homeID, awayID, roundCode, fullDate)

                    hitterStats = [0 for i in range(0, len(HS))]
                    pitcherStats = [0 for i in range(0, len(PS))]
                    points = 0

                    playerID = player[1]
                    positionCode = player[3]
                    
                    if positionCode != "P":
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

    if date == 0 or round == 0:
        print("Canceling")

    return True

def pushStatsChanges(year):
    print(f"Pushing stats changes\n---------------------\n")

    scoresData = db.generateJSONData(year)
    with open(f"data/{year}.json", "w") as f:
        json.dump(scoresData, f)

    print("Stats changes pushed")
    
    return True

def addDraft(year):
    print(f"Adding draft result\n-------------------")

    finishedDraft = False
    allParticipants = db.getAllParticipants(year)
    if len(allParticipants) == 0:
        print(f"No participants registered for {year} yet")
        finishedDraft = True
    else:
        selectedParticipant = getNumberInputFromList("Participant drafting:", [p[1] for p in allParticipants])

        if selectedParticipant != 0:
            participantID = allParticipants[selectedParticipant - 1][0]

            allRounds = db.getAllRounds()
            selectedRound = getNumberInputFromList("Round:", [r[1] for r in allRounds])

            if selectedRound != 0:
                roundNum = allRounds[selectedRound - 1][0]

                draftees = []
                allPositions = db.getAllPositions()
                i = 0
                draftingCanceled = False
                # for position in allPositions:
                while i < len(allPositions) and not draftingCanceled:
                    currentPosition = allPositions[i]
                    print(f"Drafting {currentPosition[0]}")
                    canAdd = False

                    # checking for players continuing
                    if roundNum > min([r[0] for r in allRounds]):
                        previousPlayer = db.getDraftedPlayerByRound(year, roundNum - 1, participantID, currentPosition[0])
                        if previousPlayer is not None:
                            print(f"Currently drafted player: {previousPlayer[1]} {previousPlayer[2]}, {previousPlayer[4]}")
                            continuePlayer = input("Enter y/n to carry on draft to next round: ")

                            if continuePlayer == "y":
                                canAdd = not db.checkDraftExists(participantID, previousPlayer[0], year, roundNum)
                                if canAdd:
                                    print("Carrying on player")
                                    # storing playerID, firstName, lastName, positionCode, teamID, teamCode
                                    draftees.append( (previousPlayer[0], previousPlayer[1], previousPlayer[2], currentPosition[0], previousPlayer[3], previousPlayer[4]) )

                            print()

                    # adding players otherwises
                    while not canAdd:
                        playerName = input(f"Enter the last name of the player you wish to draft (0 to cancel): ")
                        
                        if playerName == "0":
                            canAdd = True
                            draftingCanceled = True

                        else:
                            players = statsapi.lookup_player(playerName, season=year)
                            if len(players) == 0:
                                print("Could not find any players with that last name")
                            else:
                                playerList = []
                                for p in players:
                                    team = db.getTeam(int(p['currentTeam']['id']))
                                    playerList.append(f"{p['firstName']} {p['lastName']}, {team}")
                                selectedPlayer = getNumberInputFromList("Players:", playerList)

                                if selectedPlayer != 0:
                                    playerToAdd = players[selectedPlayer - 1]
                                    db.addPlayer(playerToAdd['id'], playerToAdd['firstName'], playerToAdd['lastName'])

                                    canAdd = not db.checkDraftExists(participantID, playerToAdd['id'], year, roundNum)
                                    if canAdd:
                                        draftees.append( ( playerToAdd['id'], playerToAdd['firstName'], playerToAdd['lastName'], currentPosition[0], playerToAdd['currentTeam']['id'], db.getTeam(int(playerToAdd['currentTeam']['id'])) ) )

                    i += 1

                if not draftingCanceled:
                    for pick in draftees:
                        # storing playerID, firstName, lastName, positionCode, teamID, teamCode
                        db.addDraft(pick[0], participantID, pick[3], pick[4], roundNum, year)
                        print(f"Drafted {pick[1]} {pick[2]}, {pick[5]} at {pick[3]}")
                    finishedDraft = True

    if finishedDraft:
        print("Drafting complete")
    else:
        print("Canceling")

    return True

def addParticipant(year):
    print(f"Adding participant\n------------------")

    name = input("Enter the name of the participant you want to add (0 to cancel): ")
    if name != "0":

        validName = db.addParticipant(name, year)

        while not validName:
            name = input("Participant already exists, please enter another name (0 to cancel): ")
            if name != "0":
                validName = db.addParticipant(name, year)
            else:
                validName = True

    if name == "0":
        print("Canceling")

    return True

def initialDBSetUp(year):
    print(f"Doing initial database setup\nTHIS WILL WIPE YOUR EXISTING DATABASE IF YOU HAVE ONE SET UP ALREADY!")
    userConfirmation = input("Enter y/n to do setup/cancel: ")

    if userConfirmation == "y":
        print("Setting up database")
        db.initialDBSetup()
        print("Set up finished")
    else:
        print("Canceling setup")

    return True

def exitGame(year):
    print("Exiting game")
    db.closeConnection()
    print("Thanks for playing!")
    return False

def main():
    commands = [
        updateStats,
        pushStatsChanges,
        addDraft,
        addParticipant,
        initialDBSetUp,
        exitGame,
    ]

    commandList = [
        "STATS (Update stats)",
        "PUSH (Push stats changes)",
        "DRAFT (Add player draft to database)",
        "PARTICIPANT (Add participant to database)",
        "SETUP (Do initial database setup)",
        "EXIT",
    ]

    print(f"Welcome to Family Fantasy Baseball!\n-----------------------------------\n")

    MIN_YEAR = 2011
    MAX_YEAR = 2050
    year = getNumberInput("game year", MIN_YEAR, MAX_YEAR)

    running = True
    if year == 0:
        running = exitGame(year)
    
    while running:
        commandNum = getNumberInputFromList("Commands:", commandList)
        commandToRun = exitGame
        if commandNum != 0:
            commandToRun = commands[commandNum - 1]
        running = commandToRun(year)
        print()
        

if __name__ == "__main__":
    main()