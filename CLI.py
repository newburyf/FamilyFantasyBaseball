import DB as db
import statsapi
from Enums import HitterStats as HS, PitcherStats as PS


def printCommands():
    commands = [
        "1: Update stats",
        "2: Add player to database",
        "3: Add player draft to database",
        "4: Add participant to database",
        "5: Do initial database setup",
        "0: Exit"
    ]
    print(f"\nCommands:")
    for c in commands:
        print(c)

def exit():
    print("Exiting, thanks for playing!")
    return False

def updateStats():
    print("Updating stats")
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
                    print(f"Added {players[i-1]['fullName']} to the database")
                else:
                    print("Player already exists")
            else:
                print("Canceling")
    else:
        print("Canceling")

    return True

def addDraft():
    print(f"Adding draft result\n------------")
    yearString = input("Enter the current year (0 to cancel): ")
    year = 0
    try:
        year = int(yearString)
    except:
        print("Please enter a valid year")

    if year != 0:
        print("Participants:")
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
                print("Players:")
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
                    print("Teams:")
                    i = 1
                    for t in allTeams:
                        print(f"{i}. {t[1]}")

                    selectedTeam = input("Please enter the number of the team the player is currently on (0 to cancel): ")
                    teamNum = 0
                    try:
                        teamNum = int(selectedTeam)
                    except:
                        print("Please enter a valid team number")
                    
                    if teamNum != 0:
                        teamID = allTeams[teamNum - 1][0]

                        allPositions = db.getAllPositions()
                        print("Positions:")
                        i = 1
                        for p in allPositions:
                            print(f"{i}. {p[1]}")

                        selectedPosition = input("Please enter the number of the position the player is being drafted at (0 to cancel): ")
                        positionNum = 0
                        try:
                            positionNum = int(selectedPosition)
                        except:
                            print("Please neter a vaild position number")
                        
                        if positionNum != 0:
                            positionCode = allPositions[positionNum - 1][0]

                            allRounds = db.getAllRounds()
                            print("Rounds:")
                            i = 1
                            for r in allRounds:
                                print(f"{i}. {r[1]}")

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
        db.initialDBSetUp()
        print("Set up finished")
    else:
        print("Canceling setup")

    return True
    
def main():
    print(f"Welcome to Family Fantasy Baseball!\n-----------------------------------")

    commands = [
        exit,
        updateStats,
        addPlayer,
        addDraft,
        addParticipant,
        initialDBSetUp
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
        
        commandToRun = commands[commandNum]
        running = commandToRun()

if __name__ == "__main__":
    main()