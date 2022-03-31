from MarchMadness import MarchMadnessRun

MarchMadnessRun.parseData() # creates dataset
output = [0]*127 # used to store team names for printing final bracket

regressions = MarchMadnessRun.setRegressions() # calculate regregression models using data from previous tournaments

# change these values to generate real brackets
gameTest = [10] # number of games to simulate per matchup, higher number here leads to less variation in generated brackets
yearTest = [2022] # what year(s) do you want to generate brackets for?
numBrackets = 100 # how many unique brackets do you want to generate?
for year in yearTest:
    for numGames in gameTest:
        MarchMadnessRun.tournament(year, regressions, output, numGames, numBrackets)



"""If you only want to simulate a single bracket for a single year,
calling this function with the desired inputs instead of using lines 9-14
will generate a sinlge bracket. You could also just enter a single year
in the yearTest list and set numBrackets to 1."""
#  MarchMadnessRun.tournament(year, regressions, output, numGames, numBrackets)