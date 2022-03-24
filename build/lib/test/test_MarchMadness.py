import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
import MarchMadness

def test_testTeams():
  years = [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2021]
  MarchMadness.fillData()
  assert MarchMadness.testTeams(MarchMadness.dataSet, years) == "Teams parsed correctly."
