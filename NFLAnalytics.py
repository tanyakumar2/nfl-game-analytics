# Author: Tanya Kumar

# This project analyzes NFL game data for each game played since the beginning of the 2017 season (barring the ongoing 2025 season) using a dataset called ‘gameScores.csv’. Each row in the dataset represents one NFL game and contains information such as teams, scores, season, win indicators, postseason status, team records, etcetera. 

import csv
import random

sourceFile = "gameScores.csv"
sansByeFile = "byeGameScores.csv"
cleanedFile = "cleanedGameScores.csv"

# This function will remove bye weeks.
def removeByeWeeks(sourceFile, sansByeFile):
    cleaned_rows = []
    bye = "BYE"

    # Will store processed rows
    with open(sourceFile, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader)

        for row in reader:
            if not row:
                # Skip empty lines if present
                continue 

            # The third column is index 2, GameStatus. If the GameStatus is BYE, there was no game played.
            # Also removing trailing characters, capitalizing, to remove rows with Bye Weeks
            if row[2].strip().upper() == bye:
                continue  # Skip bye-week games
            
            cleaned_rows.append(row)

    # Push cleaned rows of data to sansByeFile
    with open(sansByeFile, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(cleaned_rows)

    return cleaned_rows

# Rows with last value 1 are postseason games. The data given for these games include irrelevant information regarding past wins.
# This function will remove that irrelevant info (which is in the second to last and third to last values or postseason game rows).
def cleanCSV(sansByeFile, cleanedFile): 
    cleanedRows = [] 

    # Will store processed rows, same as in removeByeWeeks function
    with open(sansByeFile, "r", newline = "", encoding = "utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader)

        for row in reader:
            if not row:
                continue 

            # Reads the last value of each row
            last_val = row[-1].strip() 
            
            if last_val == "1": # If game is playoff game
                
                # Keeps everything but last three values, then adds the last value
                row = row[:-3] + row[-1:] 

            # Stores every row with last value 0 + edited rows with last value 1 in cleanedRows
            cleanedRows.append(row) 
    
    with open(cleanedFile, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # Writes saved header row
        writer.writerow(headers) 

        # Pushes cleanedRows to cleanedFile
        writer.writerows(cleanedRows) 
        
    return cleanedRows

# Will read the cleanedFile, convert each row/game into a dictionary, and return a list where each element is a game's dictionary
def parseGames(cleanedFile):
    games = []
    with open(cleanedFile, "r", newline = "", encoding = "utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader)

        for row in reader:
            
            # Initializes dictionary for each game
            gameDict = {}

            for i in range(len(headers)):

                # Assigns the first value to the first header name, second val to second header, etcetera.
                key = headers[i]
                value = row[i].strip()
                gameDict[key] = value
            
            # Adds each dictionary to the games list
            games.append(gameDict)

    return games

# Will take the string representing each team's record in each game and convert that to a tuple.
def parseRecords(recordString):
    recordString = recordString.strip()
    if not recordString:
        return (0, 0, 0)
    
    # Splits the string into parts around '-' 
    # ('9 - 7 - 0' will be converted to (9,7,0))
    parts = recordString.split('-')

    wins = int(parts[0])
    losses = int(parts[1])
    ties = int(parts[2]) if len(parts) > 2 else 0

    return (wins, losses, ties)

# Converts some of the values in the dictionaries from strings to integers 
def convertGameTypes(games):

    # A lot of the number values were written as decimals. 
    # I converted them to integers because there was no instance of the decimal being anything but .0.
    games['Season'] = int(games['Season'])
    games['AwayScore'] = int(float(games['AwayScore']))
    games['HomeScore'] = int(float(games['HomeScore']))
    games['AwayWin'] = int(float(games['AwayWin']))
    games['HomeWin'] = int(float(games['HomeWin']))
    games['PostSeason'] = int(games['PostSeason'])

    # Takes in the record string (#ofWins - #ofLosses - #ofTies) and converts it to a tuple by calling the parseRecords function.
    games['AwayRecord'] = parseRecords(games['AwayRecord'])
    games['HomeRecord'] = parseRecords(games['HomeRecord'])

    games['TotalPoints'] = games['AwayScore'] + games['HomeScore']
    games['PointDiff'] = abs(games['AwayScore'] - games['HomeScore'])

    # Since the dataset uses AwayWin and HomeWin to say who won the game 
    # Will determine if the home or away team won. (Win: 1, Loss: 0)
    # If home's score is equal to away's score, it's a tie
    games['Winner'] = (
        games['HomeTeam'] if games['HomeScore'] > games['AwayScore'] 
        else (games['AwayTeam'] if games['HomeScore'] < games['AwayScore'] 
        else "TIE")
    )

    return games

# Calls all the above functions
def loadGames():
    removeByeWeeks(sourceFile, sansByeFile)
    cleanCSV(sansByeFile, cleanedFile)
    games = parseGames(cleanedFile)
    games = [convertGameTypes(g) for g in games]
    return games

# Takes the list of games and a Team Name and will store every game that team has played in a list.
def gamesByTeam(games, teamName):
    teamsGames = []
    for game in games:
        
        # If either the HomeTeam or the AwayTeam in a game was the chosen team, that team played in the game.
        if game["HomeTeam"] == teamName or game["AwayTeam"] == teamName:

            # If the chosen team played in the game, that game will be added to the list.
            teamsGames.append(game)
    return teamsGames

# Takes the list of games and a Team Name and will return the percentage of games that team has won since 2017.
# This function doesn't output actual percentages because, in the NFL and in sports, in general, winning pcts are usually output as 3 digit decimals.
def teamWinPercentage(games, teamName):
    tie = "TIE"

    # Calls the previously created function to create a list of each game that team has played.
    teamGames = gamesByTeam(games,teamName)
    if not teamGames:
        return 0.0
    
    # Initialize variables for number of wins and number of ties
    # NFL formula for team's win % is ( ( (# of wins) + (0.5 * # of ties) ) / (total # of games) )
    wins = 0 
    ties = 0

    for game in teamGames:
        if game["Winner"] == teamName:
            wins += 1
        elif game["Winner"] == tie:
            ties += 1
    total = len(teamGames)
    winPercent = (wins + (0.5 * ties)) / total
    return winPercent

# Determines which game has the highest total score.
def highestScoringGame(games):
    if not games:
        return None
    highest = games[0]
    for g in games:
        if g["TotalPoints"] > highest["TotalPoints"]:
            highest = g
    return highest

# Compares the overall winning percentages of any two teams.
def compareTeams(games, teamA, teamB):

    # Grabs winning percentage by creating an instance of teamWinPercentage
    aWinPercent = teamWinPercentage(games, teamA)
    bWinPercent = teamWinPercentage(games, teamB)

    # Determines which team has the higher win percentage.
    if aWinPercent > bWinPercent:
        better = teamA
    elif bWinPercent > aWinPercent:
        better = teamB
    else:
        better = "Tie"

    return {
        "TeamA": teamA,
        "TeamB": teamB,
        "TeamAWinPercent": aWinPercent,
        "TeamBWinPercent": bWinPercent,
        "BetterTeam": better
    }

# Takes two teams and returns information about the all the matches these teams played against each other.
def headToHead(games, teamA, teamB):
    headToHeadGames = []
    for game in games:

        # Collect only games where teamA and teamB played each other
        teamsInGame = {game["HomeTeam"], game["AwayTeam"]}
        if teamA in teamsInGame and teamB in teamsInGame:
            headToHeadGames.append(game)

    # Incase the teams haven't played each other since 2017
    if not headToHeadGames:
        return {
            "TeamA": teamA,
            "TeamB": teamB,
            "GamesPlayed": 0,
            "TeamAWins": 0,
            "TeamBWins": 0,
            "Ties": 0,
            "TeamAWinPercent": 0.0,
            "TeamBWinPercent": 0.0
        }

    # Initializes variables
    teamAWins = 0
    teamBWins = 0
    ties = 0

    for game in headToHeadGames:

        #Counts the wins and ties
        if game["Winner"] == teamA:
            teamAWins += 1
        elif game["Winner"] == teamB:
            teamBWins += 1
        else:
            ties += 1

    totalGames = len(headToHeadGames)

    # NFL win percentage formula
    teamAWinPercent = (teamAWins + 0.5 * ties) / totalGames
    teamBWinPercent = (teamBWins + 0.5 * ties) / totalGames

    return {
        "TeamA": teamA,
        "TeamB": teamB,
        "GamesPlayed": totalGames,
        "TeamAWins": teamAWins,
        "TeamBWins": teamBWins,
        "Ties": ties,
        "TeamAWinPercent": teamAWinPercent,
        "TeamBWinPercent": teamBWinPercent
    }


'''
# Testing

print("First, loading games")

# Creating our first instance of the function loadGames, which initializes all the beginning functions.
games = loadGames()
print("Total games loaded:", len(games))

r = random.randint(0, 2600)
print("Sample game: ", games[r])


# Testing gamesByTeam()
print("\nTesting gamesByTeam()")
team = "Patriots"
patsGames = gamesByTeam(games, team)
print(f"Number of games played by {team}:", len(patsGames))
print("First game:", patsGames[0] if patsGames else "None")

# Testing teamWinPercentage()
print("\nTesting teamWinPercentage()")
for t in ["Patriots", "Chiefs"]:
    winPercent = teamWinPercentage(games, t)
    print(f"{t} win %: {winPercent:.3f}")

# Testing highestScoringGame()
print("\nTesting highestScoringGame()")
# Created the list patsGames when testing gamesByTeams
highestPatstGame = highestScoringGame(patsGames)
if highestPatstGame:
    print("Highest scoring Patriots game:", highestPatstGame["AwayTeam"], "vs", highestPatstGame["HomeTeam"])
    print("Season and Date: ", highestPatstGame["Season"], highestPatstGame["Date"])
    print("Total points:", highestPatstGame["TotalPoints"])
    print("Winner:", highestPatstGame["Winner"])
else:
    print("No games found.")

# Testing compareTeams()
print("\nTesting compareTeams()")
matchups = [
    ("Patriots", "Jets"),
    ("Chiefs", "Bills")
]

for teamA, teamB in matchups:
    result = compareTeams(games, teamA, teamB)
    print(f"{teamA} vs {teamB}:")
    print(f"Team A Winning Percenaget: {result['TeamAWinPercent']:.3f}")
    print(f"Team B Winning Percentage {result['TeamBWinPercent']:.3f}")
    print("Better team:", result["BetterTeam"])
    print()

# Testing headToHead()
print("\nTesting headToHead()")

headToHeadMatchups = [
    ("Patriots", "Chiefs"),
    ("Jets", "Bills"),
]

for teamA, teamB in headToHeadMatchups:
    result = headToHead(games, teamA, teamB)
    
    print(f"\n{teamA} vs {teamB}")
    print("Games played:", result["GamesPlayed"])
    print(f"{teamA} wins:", result["TeamAWins"])
    print(f"{teamB} wins:", result["TeamBWins"])
    print("Ties:", result["Ties"])
    print(f"{teamA} win %:", round(result["TeamAWinPercent"], 3))
    print(f"{teamB} win %:", round(result["TeamBWinPercent"], 3))

print("\nTESTS COMPLETED")
'''