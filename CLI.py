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
                print("Please enter a valid player number.")

            if playerNum != 0:
                toAdd = players[playerNum-1]
                db.addPlayer(toAdd['id'], toAdd['firstName'], toAdd['lastName'])

                print(f"Added {players[i-1]['fullName']} to the database")
            else:
                print("Canceling")
    else:
        print("Canceling")

    return True

def addDraft():
    print(f"Adding draft\n------------")
    return True

def addParticipant():
    print("Adding participant")
    userInput = input("Enter the name of the participant you want to add (0 to cancel): ")
    if input == "0":
        print("Canceling")
    else:
        db.addParticipant(userInput)
        print(f"\"{userInput}\" added as a participant")

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