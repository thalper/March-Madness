import numpy as np
import csv

def parseYear(year, teamSet): # input year, output numpy array storing statistics of the 68 march madness teams from that year
    dataStr = "Previous/cbb"+str(year%2000)+".csv"
    file = open(dataStr, 'r')
    line = file.readline() # reads header so it is not interpreted as data
    
    while line:
        line = file.readline()
        if line[:10] in teamSet:
            print(line)
            # add new row to numpy array that includes data for the team
    file.close()

if __name__ == "__main__":
    playoffTeams = [] #list of sets, each set contains the name of the schools that competed in March Madness
    for year in range(2013,2022):
        print(year)
        teamSet = playoffTeams[year%2013]
        parseYear(year, teamSet)
    
