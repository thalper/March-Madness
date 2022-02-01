import numpy as np
import csv


def parseYear(year, teamSet): # input year, output numpy array storing statistics of the 68 march madness teams from that year
    dataStr = "Previous/cbb"+str(year%2000)+".csv"
    with open(dataStr, newline='') as csvfile:
        dataByTeam = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in dataByTeam:
            if row[0] in teamSet:
                print(row)

if __name__ == "__main__":
    test = {"Duke", "Purdue", "Michigan", "UNLV"}
    playoffTeams = [test]*9 #list of sets, each set contains the name of the schools that competed in March Madness
    for year in range(2013,2022):
        print(year)
        teamSet = playoffTeams[year%2013]
        parseYear(year, teamSet)
    
