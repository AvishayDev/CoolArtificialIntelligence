#heuristic soloution
import random

import numpy as np
from pip._vendor.msgpack.fallback import xrange

n = 50
number_of_iterations = 0
number_of_moves = 0

#initilize the border
def resetLists():

    rows = []
    columns = []
    reduces = []
    adds = []
    for i in xrange(n):
       rows.append(i)
       columns.append(i)

    return rows, columns, reduces, adds

def createBoard(n):
    return np.zeros((n, n))

def placeQueen(rows,columns,reduces,adds):

    i = 0
    while i < n:
        randomColumns = random.choice(columns)
        randomRows = random.choice(rows)
        if (randomColumns + randomRows) not in adds and (randomColumns - randomRows) not in reduces:
            return randomColumns, randomRows
        i += 1

    return -1,-1



def display(borad):
    #disply board
    for row in xrange(n):
        for column in xrange(n):
            if borad[row][column] == 2:
                print('♛', end=' ')
            else:
                print(' .', end=' ')
        print()



def main():

    board = createBoard(n)
    rows, columns, reduces, adds = resetLists()

    num = 0
    positionColumn = 0
    positionRow = 0

    i = 0
    while i < n:
        num +=1
        positionColumn, positionRow = placeQueen(rows,columns,reduces,adds)
        if positionRow == -1:
            rows, columns, reduces, adds = resetLists()
            board = createBoard(n)
            i=0
        else:
            board[positionRow][positionColumn] = 2
            rows.remove(positionRow)
            columns.remove(positionColumn)
            reduces.append(positionColumn - positionRow)
            adds.append(positionColumn + positionRow)
            i+=1

    display(board)
    print(num)

if __name__ == '__main__':
    main()




