import numpy as np
import csv


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

if __name__ == "__main__":
    dataSet = [] # each year is a dict
    #stat order: games played, wins, adjusted offense efficiency, adjusted defensive efficiency, Power Rating, Effective Field Goal Percentage
    for year in range(2013,2022):
        dataSet.append({}) # each key is a team, the value is the data for that team
        if year == 2020:
            continue
        parseYear(year, dataSet)
    #print(dataSet)
    

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



    
