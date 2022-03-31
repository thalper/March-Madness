import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
from MarchMadness import MarchMadnessRun


# def test_testTeams():
#   pass
#   years = [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2021]
#   MarchMadness.fillData()
#   assert MarchMadness.testTeams(MarchMadness.dataSet, years) == "Teams parsed correctly."

def test_sampleRun():
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
