#file for creating AI (naive Bayes, etc) for creating weights for later simulation

def createWeights():
    numWeights = 24 # 
    weights = [0.5]*numWeights  # initialization before we do Naive Bayes analysis
    temp = w3pta(12, weights[0], 8, weights[1])
    return weights 

def w3pta(Ataken, wAT, Ballowed, WBA):
    return Ataken*wAT + Ballowed*WBA