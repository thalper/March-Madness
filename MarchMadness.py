import numpy as np
import csv
import Simulate
import AIWeighting

dataSet = [] # each year is a dict
#stat order: games played, wins, adjusted offense efficiency, adjusted defensive efficiency, Power Rating, Effective Field Goal Percentage

def parseYear(year, dataSet): # input year, output dict of numpy array storing statistics of the 68 march madness teams from that year
    dataStr = "Previous/cbb"+str(year%2000)+".csv"
    with open(dataStr, newline='') as csvfile:
        dataByTeam = csv.reader(csvfile, delimiter=',', quotechar='|')
        ind = year%2013   
        if year > 2020:
            ind -= 1
        for row in dataByTeam:
            if (year < 2020 and row[22] != "NA" and row[22] != "SEED") or (year == 2021 and row[21] != "NA" and row[21] != "SEED"):
                dataSet[ind][row[0]] = np.array(row[2:21])

def testTeams(dataSet, years):
    for i in range(len(years)):
        teamFileStr = "Previous/teams"+str(years[i]%2000)+".txt"
        teamFile = open(teamFileStr, 'r')
        teams = teamFile.read().split("\n")
        teamFile.close()
        if len(teams) != len(dataSet[i]):
            return "Different number of teams in year {}.".format(years[i])
        for team in teams:
            if team not in dataSet[i].keys():
                return team+" not in dataset in year {}.".format(years[i])
    return "Teams parsed correctly."

def parseData():
    for year in range(2013,2022):
        dataSet.append({}) # each key is a team, the value is the data for that team
        if year == 2020:
            continue
        parseYear(year, dataSet)
    #print(testTeams(dataSet, years))
    #print(dataSet)



    
if __name__ == "__main__":
    parseData() #creates dataset
    weights = AIWeighting.createWeights() #runs AI weighting
    #Simulate.simulateGame(dataSet[year][teamA], dataSet[year][teamB], weights) #simulates basketball game between two teams
    for i in range(15): #number of simulations to run
        score = Simulate.simulateGame(np.array([0.55, 0.42, 13, 60, 15]), np.array([0.49, 0.37, 18, 50, 12]), weights)
        print(score[0], "-", score[1])
"""def getTeams():
    teamsByYear = []
    for year in range(2013,2020):
        dataStr = "Previous/teams"+str(year%2000)+".txt"
        currYear = set()
        with open(dataStr, 'r') as teamsFile:
            teams = teamsFile.readlines()
            for team in teams:
                currYear.add(team.rstrip())
        teamsByYear.append(currYear)
    return teamsByYear"""



    
