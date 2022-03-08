import numpy as np
import csv
import Simulate
import AIWeighting


dataSet = [] # each year is a dict


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

def parseBracket(teamFile, year, regressions):
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
        score = Simulate.simulateGame(dataSet[dataInd][teamA], dataSet[dataInd][teamB], regressions) 
        #print(teamA, score[0], "-", score[1], teamB)
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
                row[5] = str(float(row[5]) - float(row[1]))
                row[7] = str(float(row[7]) - float(row[3]))
                dataSet[ind][row[0]] = np.array(row[1:22], dtype=float)
                tourneyTeams.remove(row[0])
    

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
    AIWeighting.parsePrevTourneyforAI(dataSet)

    
if __name__ == "__main__":
    for year in range(2013,2022):
        dataSet.append({})
    parseData()
    output = [0]*127

    regressions = []
    numStats = 4
    xData = []
    yData = []
    for i in range(numStats):
        xData.append([])
        yData.append([])
    for key in AIWeighting.prevData:
        Away = key[0]
        Home = key[1]
        year = key[2]
        # 3 point attempts DONE
        away3ptAttemptsAVG = [dataSet[year%2013][Away][0], dataSet[year%2013][Home][2]]
        away3ptAttemptsREAL = AIWeighting.prevData[key][0][0]
        xData[0].append(away3ptAttemptsAVG)
        yData[0].append(away3ptAttemptsREAL)
        home3ptAttemptsAVG = [dataSet[year%2013][Home][0], dataSet[year%2013][Away][2]]
        home3ptAttemptsREAL = AIWeighting.prevData[key][1][0]
        xData[0].append(home3ptAttemptsAVG)
        yData[0].append(home3ptAttemptsREAL)

        # 3 point percentage DONE
        away3ptPercentAVG = [dataSet[year%2013][Away][1], dataSet[year%2013][Home][3]]
        away3ptPercentREAL = AIWeighting.prevData[key][0][1]
        xData[1].append(away3ptPercentAVG)
        yData[1].append(away3ptPercentREAL)
        home3ptPercentAVG = [dataSet[year%2013][Home][1], dataSet[year%2013][Away][3]]
        home3ptPercentREAL = AIWeighting.prevData[key][1][1]
        xData[1].append(home3ptPercentAVG)
        yData[1].append(home3ptPercentREAL)

        # 2 point attempts DONE
        away2ptAttemptsAVG = [dataSet[year%2013][Away][4], dataSet[year%2013][Home][6]]
        away2ptAttemptsREAL = AIWeighting.prevData[key][0][2]
        xData[2].append(away2ptAttemptsAVG)
        yData[2].append(away2ptAttemptsREAL)
        home2ptAttemptsAVG = [dataSet[year%2013][Home][4], dataSet[year%2013][Away][6]]
        home2ptAttemptsREAL = AIWeighting.prevData[key][1][2]
        xData[2].append(home2ptAttemptsAVG)
        yData[2].append(home2ptAttemptsREAL)

        # 2 point percentage DONE
        away2ptPercentAVG = [dataSet[year%2013][Away][5], dataSet[year%2013][Home][7]]
        away2ptPercentREAL = AIWeighting.prevData[key][0][3]
        xData[3].append(away2ptPercentAVG)
        yData[3].append(away2ptPercentREAL)
        home2ptPercentAVG = [dataSet[year%2013][Home][5], dataSet[year%2013][Away][7]]
        home2ptPercentREAL = AIWeighting.prevData[key][1][3]
        xData[3].append(home2ptPercentAVG)
        yData[3].append(home2ptPercentREAL)
    
        
    regressions = [0]*numStats
    for i in range(numStats):
        currRegr = AIWeighting.manualRegression(xData[i],yData[i]) #runs AI weighting
        regressions[i] = currRegr   


    ind = 0
    for year in range(2013,2022):
        if year == 2020:
            continue
        teamsFileStr = "Previous/teams"+str(year%2000)+".txt"
        teamFile = open(teamsFileStr, "r")
        bracket = parseBracket(teamFile, year, regressions)
        dataSet[ind]["bracket"] = bracket
        ind += 1


    Simulate.simulateTournament(dataSet[6]["bracket"][0], dataSet[6]["bracket"][1], dataSet, 2019, output, regressions)
    outFile = open("Simulations/2021output.txt", 'w')
    for team in output:
        outFile.write(team)
        outFile.write("\n")
    outFile.close()
    #parseData() #creates dataset

    
    #Simulate.simulateGame(dataSet[2019%2013]["Purdue"], dataSet[6]["Virginia"], [0.0,0.5])
    #Simulate.simulateGame(dataSet[year][teamA], dataSet[year][teamB], weights) #simulates basketball game between two teams
    #for i in range(15): #number of simulations to run
        #score = Simulate.simulateGame(np.array([0.55, 0.42, 13, 60, 15]), np.array([0.49, 0.37, 18, 50, 12]), weights)
        #print(score[0], "-", score[1])