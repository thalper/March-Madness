import random
import AIWeighting
from sklearn.linear_model import LinearRegression

#Stat order
# 3 point attempts,3 point %,3 point attempts allowed,3 point % allowed,2 point attempts,2 point %
# 2 point attempts allowed,2 point % allowed,Fouls per game,opponent fouls per game,Attempted Free throws
# Opponent Attempted Free throws,Free throw %,Turnover,Turnover (Against),Possessions,Offensive rebounds,Offensive rebounds (against)
# Defensive rebounds,Defensive rebounds (against),Win %,Close game win %

# Weight order
# 


outputOrder = [1,2,33,3,4,34,49,5,6,35,7,8,36,50,57,9,10,37,11,12,38,51,13,14,39,15,16,40,52,58,61,
                17,18,41,19,20,42,53,21,22,43,23,24,44,54,59,25,26,45,27,28,46,55,29,30,47,31,32,48,56,60,62,63,
                96,97,80,98,99,81,72,100,101,82,102,103,83,73,68,104,105,84,106,107,85,74,108,109,86,110,111,87,75,69,66,
                112,113,88,114,115,89,76,116,117,90,118,119,91,77,70,120,121,92,122,123,93,78,124,125,94,126,127,95,79,71,67,65,64]

for i in range(127):
    if i+1 not in outputOrder:
        print(i+1)
used = set()

index = [0]


def assignWeights(A,B,regressions):
    # % that its a 2pt attempt, 2pt percentage, % 3pt attempt, 3 pt percentage
    Anum2s = regressions[2].predict([[A[4], B[6]]]) # number of 2s by team A
    Anum3s = regressions[0].predict([[A[0], B[2]]]) # number of 3s by team A
    A2ptP = regressions[3].predict([[A[5], B[7]]]) # 2 point percentage by team A
    A3ptP = regressions[1].predict([[A[1], B[3]]]) # 3 point percentage by team A
    
    return [Anum2s / (Anum2s + Anum3s), A2ptP, 1 - (Anum2s / (Anum2s + Anum3s)), A3ptP]

def simulatePossession(Poss):

    #Types of possession
        # Turnover
        # foul
        
    # 2pt attempt    
    if random.random() < (1 - Poss[0]):
        if random.random() < Poss[1]:
            return 2
        return 0
    # 3pt attempt
    if random.random() < Poss[3]:
        return 3
    return 0


def simulateGame(teamAdata, teamBdata, regressions):
    possessions = 60
    Ascore = 0
    Bscore = 0
    Possession = [0,0]
    Possession[0] = assignWeights(teamAdata, teamBdata, regressions)
    Possession[1] = assignWeights(teamBdata, teamAdata, regressions)
    
    for i in range(possessions):
        Ascore += simulatePossession(Possession[0])
        Bscore += simulatePossession(Possession[1])
        if index[0] == 126:
            print("Possession #", i+1, " ", Ascore, "-", Bscore)
    return [Ascore, Bscore]

def simulateTournament(a, b, dataSet, year, output, regressions):
    if type(a) == list:
        a = simulateTournament(a[0],a[1], dataSet, year, output, regressions)
    if type(b) == list: 
        b = simulateTournament(b[0],b[1], dataSet, year, output, regressions)
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
    while score[0] == score[1]:
        score = simulateGame(dataSet[ind][a], dataSet[ind][b], regressions)
    print(a, score[0], "-", score[1], b)
    output[outputOrder[index[0]]-1] = a if score[0] > score[1] else b
    index[0] += 1
    return a if score[0] > score[1] else b


# Basic Possession Formula=0.96*[(Field Goal Attempts)+(Turnovers)+0.44*(Free Throw Attempts)-(Offensive Rebounds)]

"""
        More Specific Possession Formula = 0.5*((Field Goal Attempts + 0.4*Free Throw Attempts – 
        1.07*(Offensive Rebounds/(Offensive Rebounds + Opponent Defensive Rebounds))*(Field Goal Attempts – FG) + Turnovers) +
         (Opponent Field Goal Attempts + 0.4*(Opponent Free Throw Attempts) – 
         1.07*(Opponent Offensive Rebounds)/(Opponent Offensive Rebounds + Defensive Rebounds))*(Opponent Field Goal Attempts – Opponent FG) + 
         Opponent Turnovers))"""
         
# Attempted Field goals, attempted free throws, offensive rebounds, devensive rebounds, field goals made, turnovers 
# this data from both teams will be able to predict number of possessions

# 3 point attempts (taken and allowed), 3 pt percent(taken and allowed), 2 pt attempts(taken and allowed), 2 pt percent(taken and allowed), foul rate (for and against)


