from MarchMadness import MarchMadnessRun

MarchMadnessRun.parseData() # creates dataset
output = [0]*127 # used to store team names for printing final bracket

regressions = MarchMadnessRun.setRegressions() # calculate regregression models using data from previous tournaments

'''
Values for gameTest represent the number of possessions to run for each matchup. 
For example, using 1 will run 1 game worth of possessions for each team (40 minutes),
5 will run 5 games of possessions (200 minutes), and 0.2 will run 0.2 games of possessions (8 minutes).

Using shorter games results in more "upsets" and using too short of games will result in 
games being essentially coin flips and will result in a poor guess for the final score of the game. 

If you decide to create more than 10 brackets at a time, the value(s) of gameTest will be used as an average.
Following a bell curve, 16 percent of brackets will be decided by coin flips, and 16 percent of brackets will 
be decided using at least double length games of your input, the rest will be somewhere in between.
If you want your gameTest input to be used directly, create brackets in batches of 9 or fewer.
'''
# change these values to generate real brackets

gameTest = [5] # number of games to simulate per matchup, see block comment above
yearTest = [2024] # what year(s) do you want to generate brackets for?
numBrackets = 25 # how many unique brackets do you want to generate?
# if you leave the champion field empty (or input a string that does not match a team name) it will be ignored and brackets will be filled out with no bias.
champion = "" # If this doesn't work, match the input to what your team is named on the output file
for year in yearTest:
    for numGames in gameTest:
        MarchMadnessRun.tournament(year, regressions, output, numGames, numBrackets, champion)



'''If you only want to simulate a single bracket for a single year,
calling this function with the desired inputs instead of using lines 23-28
will generate a single bracket. You could also just enter a single year
in the yearTest list and set numBrackets to 1.'''
#  MarchMadnessRun.tournament(year, regressions, output, numGames, numBrackets)