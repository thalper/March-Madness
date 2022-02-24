import random

#Stat order
# 3 point attempts,3 point %,3 point attempts allowed,3 point % allowed,field goal attempts,2 point %
# field goal attempts allowed,2 point % allowed,Fouls per game,opponent fouls per game,Attempted Free throws
# Opponent Attempted Free throws,Free throw %,Turnover,Turnover (Against),Possessions,Offensive rebounds,Offensive rebounds (against)
# Defensive rebounds,Defensive rebounds (against),Win %,Close game win %

# Weight order
# 


outputOrder = [1,2,33,3,4,34,49,5,6,35,7,8,36,50,57,9,10,37,11,12,38,51,13,14,39,15,16,40,52,58,61,
                17,18,41,19,20,42,53,21,22,43,23,24,44,54,59,25,26,45,27,28,46,55,29,30,47,31,32,48,56,60,62,63,
                96,97,80,98,99,81,72,100,101,82,102,103,83,73,68,104,105,84,106,107,85,74,108,109,86,110,111,87,75,69,66,
                112,113,88,114,115,89,76,116,117,90,118,119,91,77,70,120,121,92,122,123,93,78,124,125,94,126,127,95,71,67,65,64]



def assignWeights(A,B,weights):
    # % that its a 2pt attempt, 2pt percentage, % 3pt attempt, 3 pt percentage
    return [[(A[4]-A[0])/A[4],A[5],(A[0]/A[4]),A[1]], [(B[4]-B[0])/B[4],B[5],(B[0]/B[4]),B[1]]]

def simulatePossession(Poss):

    #Types of possession
        # 2pt attempt
        # 3pt attempt
        # Turnover
        # foul
    if random.random() < (1 - Poss[0]):
        if random.random() < Poss[1]:
            return 2
        return 0
    if random.random() < Poss[3]:
        return 3
    return 0


def simulateGame(teamAdata, teamBdata, weights):
    possessions = 60
    Ascore = 0
    Bscore = 0
    Possession = assignWeights(teamAdata, teamBdata, weights)
    
    for i in range(possessions):
        Ascore += simulatePossession(Possession[0])
        Bscore += simulatePossession(Possession[1])
        #print("Possession #", i, " ", Ascore, "-", Bscore)
    return [Ascore, Bscore]




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


# skeleton for simulating the entire bracket
"""
bracket = [[[a,b],[c,d]],[[e,f],[g,[h,i]]]]

simulateGame(bracket[0], bracket[1])

def simulateGame(a,b):
    if len(a) > 1:
        a = simulateGame(a[0],a[1])
    if len(b) > 1: 
        b = simulateGame(b[0],b[1])
    for i in range(possessions):
        simulatePossession()

    return winner"""