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

if __name__ == "__main__":
    dataSet = [] # each year is a dict
    #stat order: games played, wins, adjusted offense efficiency, adjusted defensive efficiency, Power Rating, Effective Field Goal Percentage
    for year in range(2013,2022):
        dataSet.append({}) # each key is a team, the value is the data for that team
        if year == 2020:
            continue
        parseYear(year, dataSet)
    years = [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2021] # tournament years in order
    print(testTeams(dataSet, years))
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



    
