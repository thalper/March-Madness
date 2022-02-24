index = [0]
outputOrder = [0,1,8,2,3,9,12,4,5,10,6,7,11,13,14]
used = set()


def simulateTournament(a,b, output):
    if type(a) != int:
        a = simulateTournament(a[0],a[1], output)
    if type(b) != int: 
        b = simulateTournament(b[0],b[1], output) 
    if a not in used:
        used.add(a)
        output[outputOrder[index[0]]] = a
        index[0] += 1
    if b not in used:
        used.add(b)
        output[outputOrder[index[0]]] = b
        index[0] += 1
    output[outputOrder[index[0]]] = a if a > b else b
    index[0] += 1
    return a if a > b else b

if __name__ == "__main__":
    bracket = [[[1,2],[3,4]],[[5,6],[7,8]]]
    output = [0]*15
    simulateTournament(bracket[0], bracket[1], output)
    print(output)

