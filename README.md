# nfl-game-analytics

Python program that cleans and analyzes NFL game data from the 2017–2024 seasons.

## Features

- Removes bye-week entries and cleans postseason records
- Converts raw CSV rows into structured Python dictionaries
- Calculates a team's overall winning percentage
- Finds the highest-scoring game
- Compares the winning percentages of two teams
- Calculates head-to-head records between two teams

## Dataset

The dataset contains more than 2,600 NFL games and includes team names, scores, dates, records, win indicators, and postseason status.

**Dataset source:** Add the original dataset source and link here.

## Technologies

- Python
- CSV file processing
- Python dictionaries, lists, tuples, and functions

## How to Run

1. Download or clone this repository.
2. Ensure `nfl_analytics.py` and `gameScores.csv` are in the same folder.
3. Open a Python terminal in that folder.
4. Import the program and load the dataset:


```python
from nfl_analytics import loadGames

games = loadGames()
print("Games loaded:", len(games))

## Example Usage

```python
from nfl_analytics import (
    loadGames,
    gamesByTeam,
    teamWinPercentage,
    highestScoringGame,
    compareTeams,
    headToHead,
)

games = loadGames()

patriots_games = gamesByTeam(games, "Patriots")

print(teamWinPercentage(games, "Patriots"))
print(highestScoringGame(games))
print(compareTeams(games, "Patriots", "Chiefs"))
print(headToHead(games, "Patriots", "Chiefs"))
