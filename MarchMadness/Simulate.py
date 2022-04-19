#!/usr/bin/env python
from inspect import formatargvalues
import random
import time
from sklearn.linear_model import LinearRegression
from MarchMadness.bracket import GAME_BOX_WIDTH_HEIGHT_RATIO
from importlib_resources import files
import MarchMadness.Simulations
import os

# STAT                                  |         Index
# 3 point attempts                      |           0
# 3 point %                             |           1
# 3 point attempts allowed              |           2
# 3 point % allowed                     |           3
# 2 point attempts                      |           4
# 2 point %                             |           5
# 2 point attempts allowed              |           6
# 2 point % allowed                     |           7
# Fouls per game                        |           8
# opponent fouls per game               |           9
# Attempted Free throws                 |           10
# Opponent Attempted Free throws        |           11
# Free throw %                          |           12
# Turnover                              |           13
# Turnover (Against)                    |           14
# Possessions                           |           15
# Offensive rebounds                    |           16
# Offensive rebounds (against)          |           17
# Defensive rebounds                    |           18
# Defensive rebounds (against)          |           19
# Win %                                 |           20
# Close game win %                      |           21
# Strength of Schedule                  |           22

# a mapping of the order of teams taken from the .txt file to a bracket
outputOrder = [1,2,33,3,4,34,49,5,6,35,7,8,36,50,57,9,10,37,11,12,38,51,13,14,39,15,16,40,52,58,61,
                17,18,41,19,20,42,53,21,22,43,23,24,44,54,59,25,26,45,27,28,46,55,29,30,47,31,32,48,56,60,62,63,
                96,97,80,98,99,81,72,100,101,82,102,103,83,73,68,104,105,84,106,107,85,74,108,109,86,110,111,87,75,69,66,
                112,113,88,114,115,89,76,116,117,90,118,119,91,77,70,120,121,92,122,123,93,78,124,125,94,126,127,95,79,71,67,65,64]

used = set()
index = [0]

# Possession stat                 |         Index
# 2 pointers attempts             |           0
# 2 point percentage              |           1
# 3 pointer attempts              |           2
# 3 point percentage              |           3
# opponent fouls per game         |           4
# attempted free throws           |           5
# Free throw %                    |           6
# Turnovers                       |           7
# Offensive Rebounds              |           8
# opponent Defensive Rebounds     |           9

# creates weights from regressions
def assignWeights(A,B,regressions):
    # % that its a 2pt attempt, 2pt percentage, % 3pt attempt, 3 pt percentage
    Anum3s = regressions[0].predict([[A[0], B[2], A[22]-B[22]]]) # number of 3s by team A
    A3ptP = regressions[1].predict([[A[1], B[3], A[22]-B[22]]]) # 3 point percentage by team A
    Anum2s = regressions[2].predict([[A[4], B[6], A[22]-B[22]]]) # number of 2s by team A
    A2ptP = regressions[3].predict([[A[5], B[7], A[22]-B[22]]]) # 2 point percentage by team A
    BFouls = regressions[4].predict([[B[8], A[9], B[22]-A[22]]]) # fouls commited by team B
    AFreeThrows = regressions[5].predict([[A[10], B[11], A[22]-B[22]]]) # number of attempted free throws by team A
    AFreeThrowP = regressions[6].predict([[A[12]]]) # free throw percentage team A
    ATurnovers = regressions[7].predict([[A[13], B[14], A[22]-B[22]]]) # number of turnovers by team A
    Aorb = regressions[8].predict([[A[16], B[17], A[22]-B[22]]]) # number of offensive rebounds by team A
    Bdrb = regressions[9].predict([[B[18], A[19], B[22]-A[22]]]) # number of defensive rebounds by team B
    return [Anum2s, A2ptP, Anum3s, A3ptP, BFouls, AFreeThrows, AFreeThrowP, ATurnovers, Aorb, Bdrb]

# return num points scored, num fouls commited 
def simulatePossession(Poss, fouls, numGames):
    # percent chance of each outcome
    shot2 = Poss[0] / (Poss[0] + Poss[2] + Poss[4] + Poss[7])
    made2 = Poss[1]
    shot3 = Poss[2] / (Poss[2] + Poss[4] + Poss[7]) # assuming not 2 point attempt
    made3 = Poss[3]
    foul = Poss[4] / (Poss[4] + Poss[7]) # assuming not shot attempt
    ftP = Poss[6]
    turnover = Poss[7] / (Poss[7]) # assuming not shot attempt or foul
    orb = Poss[8] / (Poss[8]+Poss[9])

    # RUNS EACH POSSESSION GIVEN THE STATS OF EACH TEAM
    # Types of possessions: 2 point attempt, 3 point attempt, foul, or turnover
    # 2pt attempt   
    if random.random() < shot2:
        # made 2 pointer
        if random.random() < made2:
            return 2, fouls
        # miss with a chance of an offensive rebound (repeats possession)
        if random.random() < orb:
            return simulatePossession(Poss, fouls, numGames)
        return 0, fouls
    # 3pt attempt
    if random.random() < shot3:
        # made 3 pointer
        if random.random() < made3:
            return 3, fouls
        # miss with a chance of an offensive rebound (repeats possession)
        if random.random() < orb:
            return simulatePossession(Poss, fouls, numGames)
        return 0, fouls
    #foul
    ftm = 0 # free throws made
    if random.random() < foul:
        fouls += 1
        # not shooting
        if random.random() < 0.25: # about 25 percent of fouls are non-shooting fouls
            # double bonus 
            if fouls >= 9*numGames:
                # take two free throw shots
                if random.random() < ftP:
                    ftm += 1
                if random.random() < ftP:
                    ftm += 1
                    return ftm, fouls
                # if second is missed, chance for an offensive rebound (repeats possession)
                elif random.random() < orb:
                    nextPpoints, fouls = simulatePossession(Poss, fouls, numGames)
                    return ftm+nextPpoints, fouls
                return ftm, fouls
            # single bonus (1 and 1)
            elif fouls >= 6*numGames:
                if random.random() < ftP:
                    if random.random() < ftP:
                        return 2, fouls
                    elif random.random() < orb:
                        nextPpoints, fouls = simulatePossession(Poss, fouls, numGames) # offensive rebound after missed free throw
                        return 1+nextPpoints, fouls # 1 free throw made plus offensive rebound
                elif random.random() < orb:
                    nextPpoints, fouls = simulatePossession(Poss, fouls, numGames) # offensive rebound after missed free throw
                    return nextPpoints, fouls
                return 0, fouls
            # not in the bonus
            return simulatePossession(Poss, fouls, numGames)
        # 2 point attempt
        elif random.random() < 0.95: # about 95% of shooting fouls occur on 2 point attempts
            if random.random() < ftP:
                ftm += 1
            if random.random() < ftP:
                ftm += 1
                return ftm, fouls
            # if second is missed, chance for an offensive rebound (repeats possession)
            elif random.random() < orb:
                nextPpoints, fouls = simulatePossession(Poss, fouls, numGames)
                return ftm+nextPpoints, fouls
            return ftm, fouls
        # 3 point attempt
        else: # 3 point attempt
            if random.random() < ftP:
                ftm += 1
            if random.random() < ftP:
                ftm += 1
            if random.random() < ftP:
                ftm += 1
                return ftm, fouls
            # if second is missed, chance for an offensive rebound (repeats possession)
            elif random.random() < orb:
                nextPpoints, fouls = simulatePossession(Poss, fouls, numGames)
                return ftm+nextPpoints, fouls
            return ftm, fouls
    #turnover
    if random.random() < turnover:
        return 0,fouls

# simulates a game (partial, full, or multiple) between two teams based on the numGames stat
def simulateGame(teamAdata, teamBdata, regressions, numGames):
    Ascore = 0
    Bscore = 0
    Possession = [0,0]
    Possession[0] = assignWeights(teamAdata, teamBdata, regressions)
    Possession[1] = assignWeights(teamBdata, teamAdata, regressions)
    possessionsPG = (teamAdata[15] + teamBdata[15]) / 2 # possessions per game
    possessions = int(numGames * possessionsPG)
    
    foulA = 0 # used for calculating if a team is in the "bonus"
    foulB = 0 # used for calculating if a team is in the "bonus"
    half = False
    for i in range(possessions):
        if i >= possessions/2 and half == False:
            half = True
            foulA = 0  # reset foul count at halftime
            foulB = 0 # reset foul count at halftime
        Pscore, foulA = simulatePossession(Possession[0], foulA, numGames)
        Ascore += Pscore
        Pscore, foulB = simulatePossession(Possession[1], foulB, numGames)
        Bscore += Pscore
    return [Ascore//numGames, Bscore//numGames]

# simulates a full bracket tournament depending on the year
def simulateTournament(a, b, dataSet, year, output, regressions, numGames, champion):
    if type(a) == list:
        a = simulateTournament(a[0],a[1], dataSet, year, output, regressions, numGames, champion)
    if type(b) == list: 
        b = simulateTournament(b[0],b[1], dataSet, year, output, regressions, numGames, champion)
    if a not in used:
        used.add(a)
        output[outputOrder[index[0]]-1] = a
        index[0] += 1
    if b not in used:
        used.add(b)
        output[outputOrder[index[0]]-1] = b
        index[0] += 1
    ind = year%2013
    if year > 2020:
        ind -= 1
    score = [0,0]
    # tie game (no OT yet)
    if (champion == a) or ("*"+champion == a):
        winner = champion
    elif (champion == b) or ("*"+champion == b):
        winner = champion
    else:
        while score[0] == score[1]:
            score = simulateGame(dataSet[ind][a], dataSet[ind][b], regressions, numGames)
        winner = a if score[0] > score[1] else b
    output[outputOrder[index[0]]-1] = winner
    if index[0] == 126:
        winnerB = winner
        if numGames < 1 or champion == winner:
            for i in range(10):
                score = simulateGame(dataSet[ind][a], dataSet[ind][b], regressions, 2)
                winnerB =  a if score[0] > score[1] else b
                if winner == winnerB:
                    break
        if winner != winnerB:
            temp = score[1]
            score[1] = score[0]
            score[0] = temp
        scoreFileStr = os.path.abspath("./brackets/"+str(year)+"outputScore.txt")
        ScoreFile = open(scoreFileStr, 'w')
        ScoreFile.write(str(int(score[0])) + "\n" + str(int(score[1])))
        ScoreFile.close()
    index[0] += 1
    return winner