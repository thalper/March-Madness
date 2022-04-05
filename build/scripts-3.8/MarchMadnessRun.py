from cv2 import ORB
import numpy as np
import csv
import MarchMadness.Simulate as Simulate
import MarchMadness.AIWeighting as AIWeighting
import MarchMadness.bracket as br
import MarchMadness.Previous
import MarchMadness.Simulations
import MarchMadness.Brackets
from importlib_resources import files

dataSet = [] # each year is a dict

def parseBracket(teamFile, year, regressions, numGames):
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
        score = Simulate.simulateGame(dataSet[dataInd][teamA], dataSet[dataInd][teamB], regressions, numGames) 
        b2[indexList[i]] = teamA if score[0] > score[1] else teamB
    bracket =   [[[[[[b2[1+16*0],b2[16+16*0]],[b2[8+16*0],b2[9+16*0]]],[[b2[4+16*0],b2[13+16*0]],[b2[5+16*0],b2[12+16*0]]]],[[[b2[2+16*0],b2[15+16*0]],[b2[7+16*0],b2[10+16*0]]],[[b2[3+16*0],b2[14+16*0]],[b2[6+16*0],b2[11+16*0]]]]],
                [[[[b2[1+16*1],b2[16+16*1]],[b2[8+16*1],b2[9+16*1]]],[[b2[4+16*1],b2[13+16*1]],[b2[5+16*1],b2[12+16*1]]]],[[[b2[2+16*1],b2[15+16*1]],[b2[7+16*1],b2[10+16*1]]],[[b2[3+16*1],b2[14+16*1]],[b2[6+16*1],b2[11+16*1]]]]]],
                [[[[[b2[1+16*2],b2[16+16*2]],[b2[8+16*2],b2[9+16*2]]],[[b2[4+16*2],b2[13+16*2]],[b2[5+16*2],b2[12+16*2]]]],[[[b2[2+16*2],b2[15+16*2]],[b2[7+16*2],b2[10+16*2]]],[[b2[3+16*2],b2[14+16*2]],[b2[6+16*2],b2[11+16*2]]]]],
                [[[[b2[1+16*3],b2[16+16*3]],[b2[8+16*3],b2[9+16*3]]],[[b2[4+16*3],b2[13+16*3]],[b2[5+16*3],b2[12+16*3]]]],[[[b2[2+16*3],b2[15+16*3]],[b2[7+16*3],b2[10+16*3]]],[[b2[3+16*3],b2[14+16*3]],[b2[6+16*3],b2[11+16*3]]]]]]]
    return bracket

def parseYear(year): # input year, output dict of numpy array storing statistics of the 68 march madness teams from that year
    # dataStr = "Previous/tr"+str(year%2000)+".csv"
    # teamsFileStr = "Previous/teams"+str(year%2000)+".txt"
    dataStr = files(MarchMadness.Previous).joinpath("tr"+str(year%2000)+".csv")
    teamsFileStr = files(MarchMadness.Previous).joinpath("teams"+str(year%2000)+".txt")
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
                row[7] = str(float(row[7]) - float(row[3]))
                dataSet[ind][row[0]] = np.array(row[1:24], dtype=float)
                tourneyTeams.remove(row[0])
    

def testTeams(years):
    for i in range(len(years)):
        # teamFileStr = "Previous/teams"+str(years[i]%2000)+".txt"
        teamFileStr = files(MarchMadness.Previous).joinpath("teams"+str(years[i]%2000)+".txt")
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
    for year in range(2013,2023):
        dataSet.append({}) # each key is a team, the value is the data for that team
        if year == 2020:
            continue
        parseYear(year)
    AIWeighting.parsePrevTourneyforAI(dataSet)

def setRegressions():
    regressions = []
    numStats = 10
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
        away3ptAttemptsAVG = [dataSet[year%2013][Away][0], dataSet[year%2013][Home][2], dataSet[year%2013][Away][22] - dataSet[year%2013][Home][22]]
        away3ptAttemptsREAL = AIWeighting.prevData[key][0][0]
        xData[0].append(away3ptAttemptsAVG)
        yData[0].append(away3ptAttemptsREAL)
        home3ptAttemptsAVG = [dataSet[year%2013][Home][0], dataSet[year%2013][Away][2], dataSet[year%2013][Home][22] - dataSet[year%2013][Away][22]]
        home3ptAttemptsREAL = AIWeighting.prevData[key][1][0]
        xData[0].append(home3ptAttemptsAVG)
        yData[0].append(home3ptAttemptsREAL)

        # 3 point percentage DONE
        away3ptPercentAVG = [dataSet[year%2013][Away][1], dataSet[year%2013][Home][3], dataSet[year%2013][Away][22] - dataSet[year%2013][Home][22]]
        away3ptPercentREAL = AIWeighting.prevData[key][0][1]
        xData[1].append(away3ptPercentAVG)
        yData[1].append(away3ptPercentREAL)
        home3ptPercentAVG = [dataSet[year%2013][Home][1], dataSet[year%2013][Away][3], dataSet[year%2013][Home][22] - dataSet[year%2013][Away][22]]
        home3ptPercentREAL = AIWeighting.prevData[key][1][1]
        xData[1].append(home3ptPercentAVG)
        yData[1].append(home3ptPercentREAL)

        # 2 point attempts DONE
        away2ptAttemptsAVG = [dataSet[year%2013][Away][4], dataSet[year%2013][Home][6], dataSet[year%2013][Away][22] - dataSet[year%2013][Home][22]]
        away2ptAttemptsREAL = AIWeighting.prevData[key][0][2]
        xData[2].append(away2ptAttemptsAVG)
        yData[2].append(away2ptAttemptsREAL)
        home2ptAttemptsAVG = [dataSet[year%2013][Home][4], dataSet[year%2013][Away][6], dataSet[year%2013][Home][22] - dataSet[year%2013][Away][22]]
        home2ptAttemptsREAL = AIWeighting.prevData[key][1][2]
        xData[2].append(home2ptAttemptsAVG)
        yData[2].append(home2ptAttemptsREAL)

        # 2 point percentage DONE
        away2ptPercentAVG = [dataSet[year%2013][Away][5], dataSet[year%2013][Home][7], dataSet[year%2013][Away][22] - dataSet[year%2013][Home][22]]
        away2ptPercentREAL = AIWeighting.prevData[key][0][3]
        xData[3].append(away2ptPercentAVG)
        yData[3].append(away2ptPercentREAL)
        home2ptPercentAVG = [dataSet[year%2013][Home][5], dataSet[year%2013][Away][7], dataSet[year%2013][Home][22] - dataSet[year%2013][Away][22]]
        home2ptPercentREAL = AIWeighting.prevData[key][1][3]
        xData[3].append(home2ptPercentAVG)
        yData[3].append(home2ptPercentREAL)

        # Fouls Committed DONE
        awayFoulsAVG = [dataSet[year%2013][Away][8], dataSet[year%2013][Home][9], dataSet[year%2013][Away][22] - dataSet[year%2013][Home][22]]
        awayFoulsREAL = AIWeighting.prevData[key][0][4]
        xData[4].append(awayFoulsAVG)
        yData[4].append(awayFoulsREAL)
        homeFoulsAVG = [dataSet[year%2013][Home][8], dataSet[year%2013][Away][9], dataSet[year%2013][Home][22] - dataSet[year%2013][Away][22]]
        homeFoulsREAL = AIWeighting.prevData[key][1][4]
        xData[4].append(homeFoulsAVG)
        yData[4].append(homeFoulsREAL)

        # Attempted Free Throws DONE
        awayFreeThrowsAVG = [dataSet[year%2013][Away][10], dataSet[year%2013][Home][11], dataSet[year%2013][Away][22] - dataSet[year%2013][Home][22]]
        awayFreeThrowsREAL = AIWeighting.prevData[key][0][5]
        xData[5].append(awayFreeThrowsAVG)
        yData[5].append(awayFreeThrowsREAL)
        homeFreeThrowsAVG = [dataSet[year%2013][Home][10], dataSet[year%2013][Away][11], dataSet[year%2013][Home][22] - dataSet[year%2013][Away][22]]
        homeFreeThrowsREAL = AIWeighting.prevData[key][1][5]
        xData[5].append(homeFreeThrowsAVG)
        yData[5].append(homeFreeThrowsREAL)

        # Free throw percentage DONE
        awayFreethrowPAVG = [dataSet[year%2013][Away][12]]
        awayFreethrowPREAL = AIWeighting.prevData[key][0][6]
        xData[6].append(awayFreethrowPAVG)
        yData[6].append(awayFreethrowPREAL)
        homeFreethrowPVG = [dataSet[year%2013][Home][12]]
        homeFreethrowPREAL = AIWeighting.prevData[key][1][6]
        xData[6].append(homeFreethrowPVG)
        yData[6].append(homeFreethrowPREAL)

        # Turnovers Committed DONE
        awayTurnoversAVG = [dataSet[year%2013][Away][13], dataSet[year%2013][Home][14], dataSet[year%2013][Away][22] - dataSet[year%2013][Home][22]]
        awayTurnoversREAL = AIWeighting.prevData[key][0][7]
        xData[7].append(awayTurnoversAVG)
        yData[7].append(awayTurnoversREAL)
        homeTurnoversAVG = [dataSet[year%2013][Home][13], dataSet[year%2013][Away][14], dataSet[year%2013][Home][22] - dataSet[year%2013][Away][22]]
        homeTurnoversREAL = AIWeighting.prevData[key][1][7]
        xData[7].append(homeTurnoversAVG)
        yData[7].append(homeTurnoversREAL)

        # ORB DONE
        awayORBAVG = [dataSet[year%2013][Away][16], dataSet[year%2013][Home][17], dataSet[year%2013][Away][22] - dataSet[year%2013][Home][22]]
        awayORBREAL = AIWeighting.prevData[key][0][8]
        xData[8].append(awayORBAVG)
        yData[8].append(awayORBREAL)
        homeORBAVG = [dataSet[year%2013][Home][16], dataSet[year%2013][Away][17], dataSet[year%2013][Home][22] - dataSet[year%2013][Away][22]]
        homeORBREAL = AIWeighting.prevData[key][1][8]
        xData[8].append(homeORBAVG)
        yData[8].append(homeORBREAL)

        # DRB
        awayDRBAVG = [dataSet[year%2013][Away][18], dataSet[year%2013][Home][19], dataSet[year%2013][Away][22] - dataSet[year%2013][Home][22]]
        awayDRBREAL = AIWeighting.prevData[key][0][9]
        xData[9].append(awayDRBAVG)
        yData[9].append(awayDRBREAL)
        homeDRBAVG = [dataSet[year%2013][Home][18], dataSet[year%2013][Away][19], dataSet[year%2013][Home][22] - dataSet[year%2013][Away][22]]
        homeDRBREAL = AIWeighting.prevData[key][1][9]
        xData[9].append(homeDRBAVG)
        yData[9].append(homeDRBREAL)
        
    regressions = [0]*numStats
    for i in range(numStats):
        currRegr = AIWeighting.manualRegression(xData[i],yData[i]) #runs AI weighting
        regressions[i] = currRegr   
    
    return regressions


def tournament(year, regressions, output, numGames, numBrackets):
    yearInd = year%2013
    if year > 2020:
        yearInd -= 1

    # teamsFileStr = "Previous/teams"+str(year%2000)+".txt"
    teamsFileStr = files(MarchMadness.Previous).joinpath("teams"+str(year%2000)+".txt")
    
    

    completedBrackets = set()
    total = 0
    total2 = 0
    minAcc = 100
    maxAcc = 0
    for i in range(numBrackets):
        teamFile = open(teamsFileStr, "r")
        bracket = parseBracket(teamFile, year, regressions, numGames)
        dataSet[yearInd]["bracket"] = bracket
        teamFile.close()
        print(i)
        while (True):
            Simulate.index[0] = 0
            Simulate.used = set()
            Simulate.simulateTournament(dataSet[yearInd]["bracket"][0], dataSet[yearInd]["bracket"][1], dataSet, year, output, regressions, numGames)
            if tuple(output) not in completedBrackets:
                completedBrackets.add(tuple(output))
                break
            else:
                print("duplicate after ", i, " brackets")
        # outFileStr = "Simulations/"+str(year)+"output.txt"
        outFileStr = files(MarchMadness.Simulations).joinpath(str(year)+"output.txt")
        outFile = open(outFileStr, 'w')
        for team in output:
            outFile.write(team)
            outFile.write("\n")
        outFile.close()
        if year <= 2022:
            currAcc = br.computeAccuracy(year)
            total += currAcc
            total2 += currAcc*currAcc
            if currAcc < minAcc:
                minAcc = currAcc
            if currAcc > maxAcc:
                maxAcc = currAcc

        # simulationFile = "Simulations/"+str(year)+"outputScore.txt"
        # bracketsFile = "Brackets/"+str(year)+"bracket"+str(i+1)+".jpg"
        scoreFile = files(MarchMadness.Simulations).joinpath(str(year)+"outputScore.txt")
        bracketsFile = files(MarchMadness.Brackets).joinpath(str(year)+"bracket"+str(i+1)+".jpg")
        br.buildBracketJPG(outFileStr, scoreFile, bracketsFile)
    
    if year <= 2022:
        stdev = ((total2 / numBrackets) - (total/numBrackets)**2)**0.5
        print("Year: " + str(year) + "   numGames: " + str(numGames))
        print("Average accuracy: " + str(total/numBrackets) + "%")
        print("Maximum accuracy: " + str(maxAcc) + "%")
        print("Minimum accuracy: " + str(minAcc) + "%")
        print("Standard Deviation: " + str(stdev) + "\n\n")

    return True

if __name__ == "__main__":
    parseData() # creates dataset
    output = [0]*127

    regressions = setRegressions()

    #gameTest = [10]
    #yearTest = [2013, 2014, 2021]
    #numBrackets = 10 # number of brackets to produce

    # use these values to generate real brackets to use this year
    gameTest = [10]
    yearTest = [2022]
    numBrackets = 100
    for year in yearTest:
        for numGames in gameTest:
            tournament(year, regressions, output, numGames, numBrackets)
        # ind = 0
        # for year in range(2013,2022):
        #     if year == 2020:
        #         continue
        #     teamsFileStr = "Previous/teams"+str(year%2000)+".txt"
        #     teamFile = open(teamsFileStr, "r")
        #     bracket = parseBracket(teamFile, year, regressions, numGames)
        #     dataSet[ind]["bracket"] = bracket
        #     ind += 1

        # Simulate.simulateTournament(dataSet[7]["bracket"][0], dataSet[7]["bracket"][1], dataSet, 2021, output, regressions)
        
        
        # Simulate.simulateTournament(dataSet[6]["bracket"][0], dataSet[6]["bracket"][1], dataSet, 2019, output, regressions)
        
        
        # outFile = open("Simulations/2021output.txt", 'w')
        # for team in output:
        #     outFile.write(team)
        #     outFile.write("\n")
        # outFile.close()
        # br.computeAccuracy()

        
        
        #Simulate.simulateGame(dataSet[2019%2013]["Purdue"], dataSet[6]["Virginia"], [0.0,0.5])
        #Simulate.simulateGame(dataSet[year][teamA], dataSet[year][teamB], weights) #simulates basketball game between two teams
        #for i in range(15): #number of simulations to run
            #score = Simulate.simulateGame(np.array([0.55, 0.42, 13, 60, 15]), np.array([0.49, 0.37, 18, 50, 12]), weights)
            #print(score[0], "-", score[1])
