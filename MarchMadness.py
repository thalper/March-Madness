import numpy as np
import csv
import Simulate
import AIWeighting


dataSet = [] # each year is a dict
#stat order: games played, wins, adjusted offense efficiency, adjusted defensive efficiency, Power Rating, Effective Field Goal Percentage

def oldParseYear(year, dataSet): # input year, output dict of numpy array storing statistics of the 68 march madness teams from that year
    dataStr = "Previous/cbb"+str(year%2000)+".csv"
    with open(dataStr, newline='') as csvfile:
        dataByTeam = csv.reader(csvfile, delimiter=',', quotechar='|')
        ind = year%2013   
        if year > 2020:
            ind -= 1
        for row in dataByTeam:
            if (year < 2020 and row[22] != "NA" and row[22] != "SEED") or (year == 2021 and row[21] != "NA" and row[21] != "SEED"):
                dataSet[ind][row[0]] = np.array(row[2:21])

def parseBracket(teamFile, year):
    b = teamFile.read().split('\n')
    i = 0
    j = 1
    b2 = [0]*65
    playInTeams = []
    indexList = []
    while i < 68:
        if b[i][0] != "*":
            b2[j] = b[i]
            i += 1
            j += 1
        else:
            playInTeams.append(b[i:i+2])
            i += 2
            indexList.append(j)
            j+=1
    dataInd = (year%2013)
    if year > 2020:
        dataInd -= 1
    for i in range(4):
        teamA = playInTeams[i][0]
        teamB = playInTeams[i][1]
        score = Simulate.simulateGame(dataSet[dataInd][teamA], dataSet[dataInd][teamB], [0.0,0.5]) # needs to be changed to include weights as last input
        print(teamA, score[0], "-", score[1], teamB)
        b2[indexList[i]] = teamA if score[0] > score[1] else teamB
    bracket =   [[[[[[b2[1+16*0],b2[16+16*0]],[b2[8+16*0],b2[9+16*0]]],[[b2[4+16*0],b2[13+16*0]],[b2[5+16*0],b2[12+16*0]]]],[[[b2[2+16*0],b2[15+16*0]],[b2[7+16*0],b2[10+16*0]]],[[b2[3+16*0],b2[14+16*0]],[b2[6+16*0],b2[11+16*0]]]]],
                [[[[b2[1+16*1],b2[16+16*1]],[b2[8+16*1],b2[9+16*1]]],[[b2[4+16*1],b2[13+16*1]],[b2[5+16*1],b2[12+16*1]]]],[[[b2[2+16*1],b2[15+16*1]],[b2[7+16*1],b2[10+16*1]]],[[b2[3+16*1],b2[14+16*1]],[b2[6+16*1],b2[11+16*1]]]]]],
                [[[[[b2[1+16*2],b2[16+16*2]],[b2[8+16*2],b2[9+16*2]]],[[b2[4+16*2],b2[13+16*2]],[b2[5+16*2],b2[12+16*2]]]],[[[b2[2+16*2],b2[15+16*2]],[b2[7+16*2],b2[10+16*2]]],[[b2[3+16*2],b2[14+16*2]],[b2[6+16*2],b2[11+16*2]]]]],
                [[[[b2[1+16*3],b2[16+16*3]],[b2[8+16*3],b2[9+16*3]]],[[b2[4+16*3],b2[13+16*3]],[b2[5+16*3],b2[12+16*3]]]],[[[b2[2+16*3],b2[15+16*3]],[b2[7+16*3],b2[10+16*3]]],[[b2[3+16*3],b2[14+16*3]],[b2[6+16*3],b2[11+16*3]]]]]]]
    return bracket

def parseYear(year): # input year, output dict of numpy array storing statistics of the 68 march madness teams from that year
    dataStr = "Previous/tr"+str(year%2000)+".csv"
    teamsFileStr = "Previous/teams"+str(year%2000)+".txt"
    teamFile = open(teamsFileStr, "r")
    tourneyTeams = set(teamFile.read().split('\n'))
    #print(tourneyTeams)
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
    teamFile = open(teamsFileStr, "r")
    bracket = parseBracket(teamFile, year)
    print(bracket)
    dataSet[ind]["bracket"] = bracket

def testTeams(years):
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
        parseYear(year)
    #print(dataSet)



    
if __name__ == "__main__":
    for year in range(2013,2022):
        dataSet.append({})
    parseYear(2021)
    output = [0]*127
    Simulate.simulateTournament(dataSet[7]["bracket"][0], dataSet[7]["bracket"][1], dataSet, year, output)
    outFile = open("Simulations/2021output.txt", 'w')
    for team in output:
        outFile.write(team)
        outFile.write("\n")
    outFile.close()
    print(output[56:])
    #parseData() #creates dataset
    weights = AIWeighting.createWeights() #runs AI weighting
    #Simulate.simulateGame(dataSet[2019%2013]["Purdue"], dataSet[6]["Virginia"], [0.0,0.5])
    #Simulate.simulateGame(dataSet[year][teamA], dataSet[year][teamB], weights) #simulates basketball game between two teams
    #for i in range(15): #number of simulations to run
        #score = Simulate.simulateGame(np.array([0.55, 0.42, 13, 60, 15]), np.array([0.49, 0.37, 18, 50, 12]), weights)
        #print(score[0], "-", score[1])




    
