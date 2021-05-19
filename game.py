import copy
import random

DEPTH = 2
VICTORY = 10 ** 20  # The value of a winning board (for max)
LOSS = -VICTORY  # The value of a losing board (for max)
TIE = 0  # The value of a tie
SIZE = 4  # the length of winning seq.
COMPUTER = SIZE + 1  # Marks the computer's cells on the board
HUMAN = 1  # Marks the human's cells on the board

rows = 6
columns = 7

# ---------- game state class -----------
class game:
    board = []
    size = rows * columns
    playTurn = HUMAN

    # Used by alpha-beta pruning to allow pruning

    '''
    The state of the game is represented by a list of 4 items:
        0. The game board - a matrix (list of lists) of ints. Empty cells = 0,
        the comp's cells = COMPUTER and the human's = HUMAN
        1. The heuristic value of the state.
        2. Whose turn is it: HUMAN or COMPUTER
        3. Number of empty cells
    '''


# ------------- game functions ------------

def create(s):
    # Returns an empty board. The human plays first.
    # create the board
    s.board = []
    for i in range(rows):
        s.board = s.board + [columns * [0]]

    s.playTurn = HUMAN
    s.size = rows * columns
    s.val = 0.00001

    # return [board, 0.00001, playTurn, r*c]     # 0 is TIE


def cpy(s1):
    # construct a parent DataFrame instance
    s2 = game()
    s2.playTurn = s1.playTurn
    s2.size = s1.size
    s2.board = copy.deepcopy(s1.board)
    # print("board ", s2.board)
    return s2


def value(s):
    # Returns the heuristic value of s
    dr = [-SIZE + 1, -SIZE + 1, 0, SIZE - 1]  # the next lines compute the heuristic val.
    dc = [0, SIZE - 1, SIZE - 1, SIZE - 1]
    val = 0.00001

    # one point with 2 or more rows of 3 is better then
    # point with one row of 3
    count3 = 0
    for row in range(rows):
        for col in range(columns):
            for i in range(len(dr)):
                t = checkSeq(s, row, col, row + dr[i], col + dc[i])
                if t in [LOSS, VICTORY]:
                    val = t
                    break
                elif t == 10:
                    count3 += 1
                    val += t * count3
                else:
                    val += t
            count3 = 0
    if s.size == 0 and val not in [LOSS, VICTORY]:
        val = TIE
    return val


def checkSeq(s, r1, c1, r2, c2):
    # r1, c1 are in the board. if r2,c2 not on board returns 0.
    # Checks the seq. from r1,c1 to r2,c2. If all X returns VICTORY. If all O returns LOSS.
    # If empty returns 0.00001. If no Os returns 1. If no Xs returns -1.
    if r2 < 0 or c2 < 0 or r2 >= rows or c2 >= columns:
        return 0  # r2, c2 are illegal

    dr = (r2 - r1) // (SIZE - 1)  # the horizontal step from cell to cell
    dc = (c2 - c1) // (SIZE - 1)  # the vertical step from cell to cell

    sum = 0

    for i in range(SIZE):  # summing the values in the seq.
        sum += s.board[r1 + i * dr][c1 + i * dc]
        if s.board[r1 + i * dr][c1 + i * dc] == 0:
            break

    if sum == COMPUTER * SIZE:
        return VICTORY

    elif sum == HUMAN * SIZE:
        return LOSS

    # row for human
    if sum > 0 and sum < COMPUTER:
        if sum == 1:
            return -1
        elif sum == 2:
            return -4
        elif sum == 3:
            return -10

    # row for computer
    elif sum > 0 and sum % COMPUTER == 0:
        number = sum / COMPUTER
        if number == 1:
            return 1
        elif number == 2:
            return 3
        elif number == 3:
            return 10

    return 0.000001  # not 0 because TIE is 0


def printState(s):
    # Prints the board. The empty cells are printed as numbers = the cells name(for input)
    # If the game ended prints who won.
    for r in range(rows):
        print("\n|", end="")
        for c in range(columns):
            if s.board[r][c] == COMPUTER:
                print("X|", end="")
            elif s.board[r][c] == HUMAN:
                print("O|", end="")
            else:
                print(" |", end="")
    print()

    for i in range(columns):  # For numbers on the bottom
        print(" ", i, sep="", end="")

    print()

    val = value(s)

    if val == VICTORY:
        print("I won!")
    elif val == LOSS:
        print("You beat me!")
    elif val == TIE:
        print("It's a TIE")


def isFinished(s):
    # Seturns True iff the game ended
    return value(s) in [LOSS, VICTORY, TIE] or s.size == 0


def isHumTurn(s):
    # Returns True iff it is the human's turn to play
    return s.playTurn == HUMAN


def decideWhoIsFirst(s):
    # The user decides who plays first
    if int(input("Who plays first? 1-me / anything else-you : ")) == 1:
        s.playTurn = COMPUTER
    else:
        s.playTurn = HUMAN
    return s.playTurn


def makeMove(s, c):
    # Puts mark (for humaמ or computer) in col. c
    # and switches turns.
    # Assumes the move is legal.
    r = 0
    while r < rows and s.board[r][c] == 0:
        r += 1

    s.board[r - 1][c] = s.playTurn  # marks the board
    s.size -= 1  # one less empty cell
    if (s.playTurn == COMPUTER):
        s.playTurn = HUMAN
    else:
        s.playTurn = COMPUTER


def inputMove(s):
    # Reads, enforces legality and executes the user's move.
    flag = True
    while flag:
        c = int(input("Enter your next move: "))
        if c < 0 or c >= columns or s.board[0][c] != 0:
            print("Illegal move.")
        else:
            flag = False
            makeMove(s, c)


def inputRandom(s):
    # See if the random should block one move ahead
    '''for i in range(0,columns):
        tmp=cpy(s)
        makeMove(tmp, i)
        if(value(tmp)==VICTORY):
            makeMove(s,i)'''
    for i in range(0, columns):  # this simple agent always plays min
        tmp = cpy(s)
        makeMove(tmp, i)
        if (value(tmp) == LOSS and s.board[0][i] == 0):  # so a "loss" is a win for this side
            makeMove(s, i)
            return
    # If no obvious move, than move random
    flag = True
    while flag:
        c = random.randrange(0, columns)
        if c < 0 or c >= columns or s.board[0][c] != 0:
            print("Illegal move.")
            printState(s)
            #break
        else:
            flag = False
            makeMove(s, c)

def getNext(s):
    # returns a list of the next states of s
    ns = []
    for c in list(range(columns)):
        # print("c=",c)
        if s.board[0][c] == 0:
            # print("possible move ", c)
            tmp = cpy(s)
            makeMove(tmp, c)
            # print("tmp board=",tmp.board)
            ns += [tmp]
            # print("ns=",ns)
    return ns


def inputComputer(s):
    return go(s)

# ------------ AlphaBeta functions -----------

def go(gm):
    # print("In go of game ", gm.board)
    if isHumTurn(gm):
        # print("Turn of human")
        obj = abmin(gm, DEPTH, LOSS - 1, VICTORY + 1)[1]
        # print("object board: ",obj.board)
        return obj
    else:
        # print("Turn of agent")
        obj = abmax(gm, DEPTH, LOSS - 1, VICTORY + 1)[1]
        # print("object board: ",obj.board)
        return obj


# s = the state (max's turn)
# d = max. depth of search
# a,b = alpha and beta
# returns [v, ns]: v = state s's value. ns = the state after recomended move.
#        if s is a terminal state ns=0.
def abmax(gm, d, a, b):
    # print("now calculate abmax")
    # print("d=",d)
    # print("alpha=",a)
    # print("beta=",b)
    if d == 0 or isFinished(gm):
        # print("returns ", [value(gm), gm])
        return [value(gm), gm]
    v = float("-inf")
    ns = getNext(gm)
    # print("next moves:", len(ns), " possible moves ")
    bestMove = 0
    for st in ns:
        tmp = abmin(st, d - 1, a, b)
        if tmp[0] > v:
            v = tmp[0]
            bestMove = st
        if v >= b:
            return [v, st]
        if v > a:
            a = v
    return [v, bestMove]


# s = the state (min's turn)
# d = max. depth of search
# a,b = alpha and beta
# returns [v, ns]: v = state s's value. ns = the state after recomended move.
#        if s is a terminal state ns=0.
def abmin(gm, d, a, b):
    # print("now calculate abmin")
    # print("d=",d)
    # print("a=",a)
    # print("b=",b)

    if d == 0 or isFinished(gm):
        # print("returns ", [value(gm), gm])
        return [value(gm), 0]
    v = float("inf")

    ns = getNext(gm)
    # print("next moves:", len(ns), " possible moves ")
    bestMove = 0
    for st in ns:
        tmp = abmax(st, d - 1, a, b)
        if tmp[0] < v:
            v = tmp[0]
            bestMove = st
        if v <= a:
            return [v, st]
        if v < b:
            b = v
    return [v, bestMove]


# ------------- playing code ------------

board = game()
create(board)
print("Initial Game")
printState(board)
decideWhoIsFirst(board)
comp_count = 0
average = 0
if int(input("10 set of 100 games enter 1, play vs me enter something else : ")) == 1:
    for i in range(10):
        for i in range(0,100):#This loops takes about 15 seconds on my computer
        #for i in range(0,50):
            while not isFinished(board):
                if isHumTurn(board):
                    inputRandom(board)
                    #inputMove(board)
                else:
                    board=go(board)
                #printState(board)
            if value(board)==10**20: #the computer (or smart agent) won
                comp_count+=1
            #print("Start another game")
            create(board)
        average += comp_count
        print("The agent beat you:", comp_count, " out of ", i + 1)
        comp_count = 0
else:
    for i in range(0,100):#This loops takes about 15 seconds on my computer
    #for i in range(0,50):
        while not isFinished(board):
            if isHumTurn(board):
                #inputRandom(board)
                inputMove(board)
            else:
                board=go(board)
            printState(board)
        if value(board)==10**20: #the computer (or smart agent) won
            break
            #comp_count+=1
        #print("Start another game")
        create(board)
    average += comp_count
    print("The agent beat you:", comp_count, " out of ", i + 1)
    comp_count = 0
print("the Average of 10 sets of 100 games is:", average/10)
print("Your grade in this section would be ", max((average/10)-80,0), " out of 20 ")
#print("Your grade in this section would be ", max(comp_count-40,0)*2, " out of 20 ")


