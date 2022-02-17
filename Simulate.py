import random

#Stat order
# 3 point attempts,3 point %,3 point attempts allowed,3 point % allowed,field goal attempts,2 point %
# field goal attempts allowed,2 point % allowed,Fouls per game,opponent fouls per game,Attempted Free throws
# Opponent Attempted Free throws,Free throw %,Turnover,Turnover (Against),Possessions,Offensive rebounds,Offensive rebounds (against)
# Defensive rebounds,Defensive rebounds (against),Win %,Close game win %

# Weight order
# 


def assignWeights(A,B,weights):
    # % that its a 2pt attempt, 2pt percentage, % 3pt attempt, 3 pt percentage
    return [[(A[4]-A[0])/A[4],A[5],(A[0]/A[4]),A[1]], [(B[4]-B[0])/B[4],B[5],(B[0]/B[4]),B[1]]]

def simulatePossession(Poss):

    #Types of possession
        # 2pt attempt
        # 3pt attempt
        # Turnover
        # foul
    print(Poss)
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
        print("Possession #", i, " ", Ascore, "-", Bscore)
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