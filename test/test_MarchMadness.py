#!/usr/bin/env python
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
  champion = ""
  for year in yearTest:
      for numGames in gameTest:
          assert MarchMadness.MarchMadnessRun.tournament(year, regressions, output, numGames, numBrackets, champion) == True

def test_tournament2():
  MarchMadness.MarchMadnessRun.parseData() # creates dataset
  output = [0]*127 # used to store team names for printing final bracket

  regressions = MarchMadness.MarchMadnessRun.setRegressions() # calculate regregression models using data from previous tournaments

  # change these values to generate real brackets
  gameTest = [1] # number of games to simulate per matchup, higher number here leads to less variation in generated brackets
  yearTest = [2021, 2022] # what year(s) do you want to generate brackets for?
  numBrackets = 25 # how many unique brackets do you want to generate?
  champion = ""
  for year in yearTest:
      for numGames in gameTest:
          assert MarchMadness.MarchMadnessRun.tournament(year, regressions, output, numGames, numBrackets, champion) == True

def test_tournament3():
  MarchMadness.MarchMadnessRun.parseData() # creates dataset
  output = [0]*127 # used to store team names for printing final bracket

  regressions = MarchMadness.MarchMadnessRun.setRegressions() # calculate regregression models using data from previous tournaments

  # change these values to generate real brackets
  gameTest = [0] # number of games to simulate per matchup, higher number here leads to less variation in generated brackets
  yearTest = [2022] # what year(s) do you want to generate brackets for?
  numBrackets = 100 # how many unique brackets do you want to generate?
  champion = ""
  for year in yearTest:
      for numGames in gameTest:
          assert MarchMadness.MarchMadnessRun.tournament(year, regressions, output, numGames, numBrackets, champion) == True
        
def test_tournament4(monkeypatch):
  monkeypatch.setattr('builtins.input', lambda _: "y")
  MarchMadness.MarchMadnessRun.parseData() # creates dataset
  output = [0]*127 # used to store team names for printing final bracket

  regressions = MarchMadness.MarchMadnessRun.setRegressions() # calculate regregression models using data from previous tournaments

  # change these values to generate real brackets
  gameTest = [1] # number of games to simulate per matchup, higher number here leads to less variation in generated brackets
  yearTest = [2022] # what year(s) do you want to generate brackets for?
  numBrackets = 5 # how many unique brackets do you want to generate?
  champion = "Purdue"
  for year in yearTest:
      for numGames in gameTest:
          assert MarchMadness.MarchMadnessRun.tournament(year, regressions, output, numGames, numBrackets, champion) == True
        



  
