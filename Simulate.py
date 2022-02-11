import random

def simulatePossession(Offense, Defense, weights):

    #Types of possession
        # 2pt attempt
        # 3pt attempt
        # Turnover
        # foul
    if random.random() < (1 - Offense[4]/Offense[3]):
        if random.random() < Offense[0]:
            return 2
        return 0
    if random.random() < Offense[1]:
        return 3
    return 0


def simulateGame(teamAdata, teamBdata, weights):
    possessions = 60
    Ascore = 0
    Bscore = 0
    for i in range(possessions):
        Ascore += simulatePossession(teamAdata, teamBdata, weights)
        Bscore += simulatePossession(teamBdata, teamAdata, weights)
        #print("Possession #", i, " ", Ascore, "-", Bscore)
    return [Ascore, Bscore]




# Basic Possession Formula=0.96*[(Field Goal Attempts)+(Turnovers)+0.44*(Free Throw Attempts)-(Offensive Rebounds)]

"""
        More Specific Possession Formula = 0.5*((Field Goal Attempts + 0.4*Free Throw Attempts – 
        1.07*(Offensive Rebounds/(Offensive Rebounds + Opponent Defensive Rebounds))*(Field Goal Attempts – FG) + Turnovers) +
         (Opponent Field Goal Attempts + 0.4*(Opponent Free Throw Attempts) – 
         1.07*(Opponent Offensive Rebounds)/(Opponent Offensive Rebounds + Defensive Rebounds))*(Opponent Field Goal Attempts – Opponent FG) + 
         Opponent Turnovers))"""