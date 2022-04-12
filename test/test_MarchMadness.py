import sys
import os
import MarchMadness.MarchMadnessRun

def test_tournament1():
  MarchMadness.MarchMadnessRun.parseData() # creates dataset
  output = [0]*127 # used to store team names for printing final bracket

  regressions = MarchMadness.MarchMadnessRun.setRegressions() # calculate regregression models using data from previous tournaments

  # change these values to generate real brackets
  gameTest = [1] # number of games to simulate per matchup, higher number here leads to less variation in generated brackets
  yearTest = [2021, 2022] # what year(s) do you want to generate brackets for?
  numBrackets = 5 # how many unique brackets do you want to generate?
  for year in yearTest:
      for numGames in gameTest:
          assert MarchMadness.MarchMadnessRun.tournament(year, regressions, output, numGames, numBrackets) == True

def test_tournament2():
  MarchMadness.MarchMadnessRun.parseData() # creates dataset
  output = [0]*127 # used to store team names for printing final bracket

  regressions = MarchMadness.MarchMadnessRun.setRegressions() # calculate regregression models using data from previous tournaments

  # change these values to generate real brackets
  gameTest = [5] # number of games to simulate per matchup, higher number here leads to less variation in generated brackets
  yearTest = [2021, 2022] # what year(s) do you want to generate brackets for?
  numBrackets = 10 # how many unique brackets do you want to generate?
  for year in yearTest:
      for numGames in gameTest:
          assert MarchMadness.MarchMadnessRun.tournament(year, regressions, output, numGames, numBrackets) == True
        


  
