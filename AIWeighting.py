import collections
import math
import numpy as np
import re
import string
import csv
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

dataSet = [] # each year is a dict


def parseData():
    for year in range(2013,2022):
        dataSet.append({}) # each key is a team, the value is the data for that team
        if year == 2020:
            continue
        parseYear(year)

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
                dataSet[ind][row[0]] = np.array(row[1:22], dtype=float)
                tourneyTeams.remove(row[0])

def parsePrevTourneyforAI():
    dataStr = "Previous\MMadnessBoxScores_15-19.csv" # previous tournament data box scores
    with open(dataStr, newline='') as csvfile:
        dataByGame = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in dataByGame:
            print(row)

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
    print("Accuracy:", 100 * r2_score(Y_test, y_pred))

if __name__ == "__main__":
    xData = [[12.4, 14.2],[13.7, 12.1],[14.3,16.2],[11.2,15.6],[12.6,15.2],[12.0, 15.2],[13.7, 12.1],[14.7,16.2],[11.2,15.6],[12.6,15.2]]
    yData = [13, 14, 15, 12, 15, 13, 14, 15, 12, 15]
    regression(xData, yData)