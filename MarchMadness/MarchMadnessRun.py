#!/usr/bin/env python
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
import os

dataSet = [] # each year is a dict

# parses a bracket from the given teams from a given year
def parseBracket(teamFile, year, regressions, numGames, champion):
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
        if teamA == champion or teamA == "*"+champion:
            b2[indexList[i]] = teamA
        elif teamB == champion or teamB == "*"+champion:
            b2[indexList[i]] = teamB
        else:
            score = Simulate.simulateGame(dataSet[dataInd][teamA], dataSet[dataInd][teamB], regressions, numGames) 
            b2[indexList[i]] = teamA if score[0] > score[1] else teamB
    bracket =   [[[[[[b2[1+16*0],b2[16+16*0]],[b2[8+16*0],b2[9+16*0]]],[[b2[4+16*0],b2[13+16*0]],[b2[5+16*0],b2[12+16*0]]]],[[[b2[2+16*0],b2[15+16*0]],[b2[7+16*0],b2[10+16*0]]],[[b2[3+16*0],b2[14+16*0]],[b2[6+16*0],b2[11+16*0]]]]],
                [[[[b2[1+16*1],b2[16+16*1]],[b2[8+16*1],b2[9+16*1]]],[[b2[4+16*1],b2[13+16*1]],[b2[5+16*1],b2[12+16*1]]]],[[[b2[2+16*1],b2[15+16*1]],[b2[7+16*1],b2[10+16*1]]],[[b2[3+16*1],b2[14+16*1]],[b2[6+16*1],b2[11+16*1]]]]]],
                [[[[[b2[1+16*2],b2[16+16*2]],[b2[8+16*2],b2[9+16*2]]],[[b2[4+16*2],b2[13+16*2]],[b2[5+16*2],b2[12+16*2]]]],[[[b2[2+16*2],b2[15+16*2]],[b2[7+16*2],b2[10+16*2]]],[[b2[3+16*2],b2[14+16*2]],[b2[6+16*2],b2[11+16*2]]]]],
                [[[[b2[1+16*3],b2[16+16*3]],[b2[8+16*3],b2[9+16*3]]],[[b2[4+16*3],b2[13+16*3]],[b2[5+16*3],b2[12+16*3]]]],[[[b2[2+16*3],b2[15+16*3]],[b2[7+16*3],b2[10+16*3]]],[[b2[3+16*3],b2[14+16*3]],[b2[6+16*3],b2[11+16*3]]]]]]]
    return bracket

# input year, output dict of numpy array storing statistics of the 68 March Madness teams from that year
def parseYear(year):
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

# parses all of the data for the available years, then sends the data for weighting
def parseData():
    for year in range(2013,2025):
        dataSet.append({}) # each key is a team, the value is the data for that team
        if year == 2020:
            continue
        parseYear(year)
    AIWeighting.parsePrevTourneyforAI(dataSet)

# creates the regressions for each weighting
def setRegressions():
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
        # 3 point attempts
        away3ptAttemptsAVG = [dataSet[year%2013][Away][0], dataSet[year%2013][Home][2], dataSet[year%2013][Away][22] - dataSet[year%2013][Home][22]]
        away3ptAttemptsREAL = AIWeighting.prevData[key][0][0]
        xData[0].append(away3ptAttemptsAVG)
        yData[0].append(away3ptAttemptsREAL)
        home3ptAttemptsAVG = [dataSet[year%2013][Home][0], dataSet[year%2013][Away][2], dataSet[year%2013][Home][22] - dataSet[year%2013][Away][22]]
        home3ptAttemptsREAL = AIWeighting.prevData[key][1][0]
        xData[0].append(home3ptAttemptsAVG)
        yData[0].append(home3ptAttemptsREAL)

        # 3 point percentage
        away3ptPercentAVG = [dataSet[year%2013][Away][1], dataSet[year%2013][Home][3], dataSet[year%2013][Away][22] - dataSet[year%2013][Home][22]]
        away3ptPercentREAL = AIWeighting.prevData[key][0][1]
        xData[1].append(away3ptPercentAVG)
        yData[1].append(away3ptPercentREAL)
        home3ptPercentAVG = [dataSet[year%2013][Home][1], dataSet[year%2013][Away][3], dataSet[year%2013][Home][22] - dataSet[year%2013][Away][22]]
        home3ptPercentREAL = AIWeighting.prevData[key][1][1]
        xData[1].append(home3ptPercentAVG)
        yData[1].append(home3ptPercentREAL)

        # 2 point attempts
        away2ptAttemptsAVG = [dataSet[year%2013][Away][4], dataSet[year%2013][Home][6], dataSet[year%2013][Away][22] - dataSet[year%2013][Home][22]]
        away2ptAttemptsREAL = AIWeighting.prevData[key][0][2]
        xData[2].append(away2ptAttemptsAVG)
        yData[2].append(away2ptAttemptsREAL)
        home2ptAttemptsAVG = [dataSet[year%2013][Home][4], dataSet[year%2013][Away][6], dataSet[year%2013][Home][22] - dataSet[year%2013][Away][22]]
        home2ptAttemptsREAL = AIWeighting.prevData[key][1][2]
        xData[2].append(home2ptAttemptsAVG)
        yData[2].append(home2ptAttemptsREAL)

        # 2 point percentage
        away2ptPercentAVG = [dataSet[year%2013][Away][5], dataSet[year%2013][Home][7], dataSet[year%2013][Away][22] - dataSet[year%2013][Home][22]]
        away2ptPercentREAL = AIWeighting.prevData[key][0][3]
        xData[3].append(away2ptPercentAVG)
        yData[3].append(away2ptPercentREAL)
        home2ptPercentAVG = [dataSet[year%2013][Home][5], dataSet[year%2013][Away][7], dataSet[year%2013][Home][22] - dataSet[year%2013][Away][22]]
        home2ptPercentREAL = AIWeighting.prevData[key][1][3]
        xData[3].append(home2ptPercentAVG)
        yData[3].append(home2ptPercentREAL)

        # Fouls Committed
        awayFoulsAVG = [dataSet[year%2013][Away][8], dataSet[year%2013][Home][9], dataSet[year%2013][Away][22] - dataSet[year%2013][Home][22]]
        awayFoulsREAL = AIWeighting.prevData[key][0][4]
        xData[4].append(awayFoulsAVG)
        yData[4].append(awayFoulsREAL)
        homeFoulsAVG = [dataSet[year%2013][Home][8], dataSet[year%2013][Away][9], dataSet[year%2013][Home][22] - dataSet[year%2013][Away][22]]
        homeFoulsREAL = AIWeighting.prevData[key][1][4]
        xData[4].append(homeFoulsAVG)
        yData[4].append(homeFoulsREAL)

        # Attempted Free Throws
        awayFreeThrowsAVG = [dataSet[year%2013][Away][10], dataSet[year%2013][Home][11], dataSet[year%2013][Away][22] - dataSet[year%2013][Home][22]]
        awayFreeThrowsREAL = AIWeighting.prevData[key][0][5]
        xData[5].append(awayFreeThrowsAVG)
        yData[5].append(awayFreeThrowsREAL)
        homeFreeThrowsAVG = [dataSet[year%2013][Home][10], dataSet[year%2013][Away][11], dataSet[year%2013][Home][22] - dataSet[year%2013][Away][22]]
        homeFreeThrowsREAL = AIWeighting.prevData[key][1][5]
        xData[5].append(homeFreeThrowsAVG)
        yData[5].append(homeFreeThrowsREAL)

        # Free throw percentage
        awayFreethrowPAVG = [dataSet[year%2013][Away][12]]
        awayFreethrowPREAL = AIWeighting.prevData[key][0][6]
        xData[6].append(awayFreethrowPAVG)
        yData[6].append(awayFreethrowPREAL)
        homeFreethrowPVG = [dataSet[year%2013][Home][12]]
        homeFreethrowPREAL = AIWeighting.prevData[key][1][6]
        xData[6].append(homeFreethrowPVG)
        yData[6].append(homeFreethrowPREAL)

        # Turnovers Committed
        awayTurnoversAVG = [dataSet[year%2013][Away][13], dataSet[year%2013][Home][14], dataSet[year%2013][Away][22] - dataSet[year%2013][Home][22]]
        awayTurnoversREAL = AIWeighting.prevData[key][0][7]
        xData[7].append(awayTurnoversAVG)
        yData[7].append(awayTurnoversREAL)
        homeTurnoversAVG = [dataSet[year%2013][Home][13], dataSet[year%2013][Away][14], dataSet[year%2013][Home][22] - dataSet[year%2013][Away][22]]
        homeTurnoversREAL = AIWeighting.prevData[key][1][7]
        xData[7].append(homeTurnoversAVG)
        yData[7].append(homeTurnoversREAL)

        # ORB
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

# runs a bracket tournament from the provided data
def tournament(year, regressions, output, _numGames, numBrackets, champion):
    if champion and champion != "Purdue":
        if "y" == input("Are you sure you want to pick " + champion + " (instead of Purdue)?\n(y/n)\n"):
            input("\nLame.\n\npress Enter to continue")
        else:
            print("Good choice.")
            return True
    if champion == "Purdue":
        print("\nBTFU!\n")
    
    print("Creating your bracket(s):\nyear: " + str(year) + " numGames: " + "{:0.2f}".format(_numGames))
    try:
        os.mkdir("./brackets")
    except:
        pass
    yearInd = year%2013
    if year > 2020:
        yearInd -= 1

    teamsFileStr = files(MarchMadness.Previous).joinpath("teams"+str(year%2000)+".txt")
    printed = 0
    toprint = 0

    completedBrackets = set()
    total = 0
    total2 = 0
    total3 = 0
    total4 = 0
    minAcc = 100
    maxAcc = 0
    minScore = 1920
    worstInd = 0
    maxScore = 0
    bestInd = 0

    # ESPN percentile thresholds for 2021 and 2022 and 2023
    threshold = False
    # thresholds
    if year == 2021:
        ninetyT = 1050
        seventyFiveT = 880
        fiftyT = 710
        threshold = True
    elif year == 2022:
        ninetyT = 850
        seventyFiveT = 650
        fiftyT = 530
        threshold = True
    elif year == 2023:
        ninetyT = 570
        seventyFiveT = 490
        fiftyT = 430
        threshold = True

    # number of brackets above threshold
    ninety = 0 
    seventyFive = 0
    fifty = 0

    # creates bell curve for brackets created
    if numBrackets < 10:
        numGames = [_numGames]*numBrackets
    else:
        numGames = np.random.normal(_numGames, _numGames, numBrackets)
    for i in range(len(numGames)):
        if numGames[i] < 0.03:
            numGames[i] = 0.03
    for i in range(numBrackets):
        teamFile = open(teamsFileStr, "r")
        bracket = parseBracket(teamFile, year, regressions, numGames[i], champion)
        dataSet[yearInd]["bracket"] = bracket
        teamFile.close()
        while (True):
            Simulate.index[0] = 0
            Simulate.used = set()
            Simulate.simulateTournament(dataSet[yearInd]["bracket"][0], dataSet[yearInd]["bracket"][1], dataSet, year, output, regressions, numGames[i], champion)
            if tuple(output) not in completedBrackets:
                completedBrackets.add(tuple(output))
                break
            else:
                print("duplicate after ", i, " brackets") # pragma: no cover
        outFileStr = files(MarchMadness.Simulations).joinpath(str(year)+"output.txt")
        outFile = open(outFileStr, 'w')
        for team in output:
            outFile.write(team)
            outFile.write("\n")
        outFile.close()
        # finds accuracy and percentile (if 2021 or 2022 or 2023) for each bracket
        if year <= 2023:
            currAcc = br.computeAccuracy(year)
            currScore = br.computeScore(year)
            total += currAcc
            total2 += currAcc*currAcc
            total3 += currScore
            total4 += currScore*currScore
            if currAcc < minAcc:
                minAcc = currAcc
            if currAcc > maxAcc:
                maxAcc = currAcc
            if currScore < minScore:
                minScore = currScore
                worstInd = i + 1
            if currScore > maxScore:
                maxScore = currScore
                bestInd = i + 1
            if threshold:
                if currScore >= fiftyT:
                    fifty += 1
                    if currScore >= seventyFiveT: 
                        seventyFive += 1
                        if currScore >= ninetyT:
                            ninety += 1
            
        scoreFile = os.path.abspath("./brackets/"+str(year)+"outputScore.txt")
        bracketsFile = "./brackets/"+str(year)+"_{:0.2f}".format(_numGames)+"bracket"+str(i+1)+".jpg"
        br.buildBracketJPG(outFileStr, scoreFile, bracketsFile)
        # creates a loading bar when brackets being made
        if (2 * toprint) >= 99.5:
            print("\b\b\b\b", end="") # pragma: no cover
        elif (2 * toprint) >= 9.5:
            print("\b\b\b", end="")
        else:
            print("\b\b", end="")
        toprint += 50 / numBrackets
        for i in range(printed, int(toprint)):
            print(b'\xdb'.decode('cp437'), end='')
        printed = int(toprint)
        print("{:0.0f}".format(2 * toprint) + "%", end='', flush=True)
    # prints out stats for brackets for testing
    if year <= 2023:
        stdev = ((total2 / numBrackets) - (total/numBrackets)**2)**0.5
        stdevScore = ((total4 / numBrackets) - (total3/numBrackets)**2)**0.5
        print("\n\nYear: " + str(year) + "   average numGames: " + "{:0.2f}".format(np.average(numGames)))
        print("Average accuracy: " + "{:0.2f}".format(total/numBrackets) + "%")
        print("Maximum accuracy: " + "{:0.2f}".format(maxAcc) + "%")
        print("Minimum accuracy: " + "{:0.2f}".format(minAcc) + "%")
        print("Standard Deviation: " + "{:0.2f}".format(stdev) + "\n")
        print("Average score: " + str(total3/numBrackets))
        print("Maximum score: " + str(maxScore) + " (bracket number "+str(bestInd) + ")")
        print("Minimum score: " + str(minScore) + " (bracket number "+str(worstInd) + ")")
        print("Standard Deviation of Score: " + "{:0.2f}".format(stdevScore) + "\n")
        if threshold:
            print("Percentiles of " + str(numBrackets) + " brackets:")
            print("Brackets in the 90th percentile:", ninety)
            print("Brackets in the 75th percentile:",  seventyFive)
            print("Brackets in the 50th percentile:", fifty, "\n")
    return True
