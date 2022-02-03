import numpy as np
import csv


def parseYear(year, dataSet): # input year, output numpy array storing statistics of the 68 march madness teams from that year
    dataStr = "Previous/cbb"+str(year%2000)+".csv"
    with open(dataStr, newline='') as csvfile:
        dataByTeam = csv.reader(csvfile, delimiter=',', quotechar='|')
        count = 0
        ind = year%2013
        if year > 2020:
            ind -= 1
        for row in dataByTeam:
            if (year < 2020 and row[22] != "NA" and row[22] != "SEED") or (year == 2021 and row[21] != "NA" and row[21] != "SEED"):
                dataSet[ind,count] = np.array(row[2:21])
                count += 1


def getTeams():
    teamsByYear = []
    for year in range(2013,2020):
        dataStr = "Previous/teams"+str(year%2000)+".txt"
        currYear = set()
        with open(dataStr, 'r') as teamsFile:
            teams = teamsFile.readlines()
            for team in teams:
                currYear.add(team.rstrip())
        teamsByYear.append(currYear)
    return teamsByYear

#DELETE LATER, USED FOR TESTING CI
def addition(a, b):
    return a + b


if __name__ == "__main__":
    dataSet = np.zeros(shape=(9,68,19))
    for year in range(2013,2022):
        if year == 2020:
            continue
        parseYear(year, dataSet)
    print(dataSet)
    
