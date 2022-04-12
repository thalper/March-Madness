import MarchMadness.MarchMadnessRun as MarchMadness
import collections
import math
import numpy as np
import re
import string
import csv
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from importlib_resources import files
import MarchMadness.Previous

prevData = {}

def parsePrevTourneyforAI(dataSet):
    # dataStr = "Previous/NCAATourneyFullBoxscoresAndStats_15-19.csv" # previous tournament data box scores
    dataStr = files(MarchMadness.Previous).joinpath("NCAATourneyFullBoxscoresAndStats_15-19.csv")
    with open(dataStr, newline='') as csvfile:
        dataByGame = csv.reader(csvfile, delimiter=',', quotechar='|')
        count = 0
        bad = 0
        for row in dataByGame:
            count +=1
            year = row[85]
            if row[83] == "Home":
                teamH = row[84]
                teamA = row[81]
            else:
                teamA = row[84]
                teamH = row[81]
            if year == "Year":
                continue
            year = int(year)
            if teamH not in dataSet[year%2013]:
                if "*"+teamH not in dataSet[year%2013]:
                    bad += 1
                    print(count, teamH, year, bad)
                else:
                    teamH = "*"+teamH
            if teamA not in dataSet[year%2013]:
                if "*"+teamA not in dataSet[year%2013]:
                    bad += 1
                    print(count, teamA, year, bad)
                else:
                    teamA = "*"+teamA
            gameKey = (teamA, teamH, year)
            # Stat order:
            # 3 point attempts, 3 point percentage, 2 point attempts, 2 point percentage, fouls committed, attempted free throws, free throw percentage, turnovers, offensive rebounds, defensive rebounds
            Astats = [float(row[28]), float(row[29]), float(row[36]), float(row[37]), float(row[22]), float(row[14]), float(row[15]), float(row[35]), float(row[21]), float(row[8])] 
            Hstats = [float(row[68]), float(row[69]), float(row[76]), float(row[77]), float(row[62]), float(row[54]), float(row[55]), float(row[75]), float(row[61]), float(row[48])]
            GameStats = [Astats, Hstats]
            prevData[gameKey] = GameStats

def manualRegression(X_train, Y_train):
    regr = LinearRegression()
    regr.fit(X_train,Y_train)
    return regr

