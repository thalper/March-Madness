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


def parseData():
    for year in range(2013,2023):
        MarchMadness.dataSet.append({}) # each key is a team, the value is the data for that team
        if year == 2020:
            continue
        parseYear(year)
    parsePrevTourneyforAI(MarchMadness.dataSet)
    

def parseYear(year): # input year, output dict of numpy array storing statistics of the 68 march madness teams from that year
    dataStr = "Previous/tr"+str(year%2000)+".csv"
    teamsFileStr = "Previous/teams"+str(year%2000)+".txt"
    teamFile = open(teamsFileStr, "r")
    tourneyTeams = set(teamFile.read().split('\n'))
    teamFile.close()
    with open(dataStr, newline='') as csvfile:
        dataByTeam = csv.reader(csvfile, delimiter=',', quotechar='|')
        ind = year%2013   
        if year > 2020:
            ind -= 1
        for row in dataByTeam:
            if row[0] in tourneyTeams:
                row[5] = str(float(row[5]) - float(row[1]))
                MarchMadness.dataSet[ind][row[0]] = np.array(row[1:22], dtype=float)
                tourneyTeams.remove(row[0])

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

#file for creating AI (naive Bayes, etc) for creating weights for later simulation
def createWeights():
    numWeights = 24 # 
    weights = [0.5]*numWeights  # initialization before we do Naive Bayes analysis
    temp = w3pta(12, weights[0], 8, weights[1])
    return weights 

def w3pta(Ataken, wAT, Ballowed, WBA):
    return Ataken*wAT + Ballowed*WBA

def regression(xData, yData):

    X_train, X_test, Y_train, Y_test = train_test_split(xData, yData, test_size = 0.2)
    
    regr = LinearRegression()
    regr.fit(X_train,Y_train)
    y_pred = regr.predict(X_test)

    print(X_test, y_pred)

def manualRegression(X_train, Y_train):
    regr = LinearRegression()
    regr.fit(X_train,Y_train)
    

    return regr

if __name__ == "__main__":
    for year in range(2013,2023):
        MarchMadness.dataSet.append({})
    parseData()
    xData = []
    yData = []
    for key in prevData:
        Away = key[0]
        Home = key[1]
        year = key[2]
        currX = [MarchMadness.dataSet[year%2013][Away][0], MarchMadness.dataSet[year%2013][Home][2]]
        currY = prevData[key][0][0]
        xData.append(currX)
        yData.append(currY)
    # xData = [[12.4, 14.2],[13.7, 12.1],[14.3,16.2],[11.2,15.6],[12.6,15.2],[12.0, 15.2],[13.7, 12.1],[14.7,16.2],[11.2,15.6],[12.6,15.2]]
    # yData = [13, 14, 15, 12, 15, 13, 14, 15, 12, 15]
    regr = manualRegression(xData, yData)
    print(regr.predict([[18.5, 22.7]]))
