import random

def HillClimbOnce(df, start):
    currentIndex = start
    currentRow = df.iloc[currentIndex]

    while True:
        bestNeighbor = currentRow
        bestIndex = currentIndex
        for i in range(len(df)):
            if i == currentIndex:
                continue
            neighbor = df.iloc[i]
            if neighbor["skorSAW"] > bestNeighbor["skorSAW"]:
                bestNeighbor = neighbor
                bestIndex = i
        if bestNeighbor["skorSAW"] > currentRow["skorSAW"]:
            currentRow = bestNeighbor
            currentIndex = bestIndex
        else:
            break

    return currentRow

def HillClimbing(df, max_restart = 10):
    bestOverall = None
    bestScore = -1

    for i in range(max_restart):
        start = random.randint(0, len(df)-1)
        hasil = HillClimbOnce(df, start)
        if hasil["skorSAW"] > bestScore:
            bestScore = hasil["skorSAW"]
            bestOverall = hasil

    return bestOverall["Toko"]