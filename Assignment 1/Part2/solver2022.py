#!/usr/local/bin/python3
# solver2022.py : 2022 Sliding tile puzzle solver
#
# Code by: CHANDRA KIRAN BACHHU CBACHHU
#
# Based on skeleton code by D. Crandall & B551 Staff, Fall 2022
#
import numpy as np
import math as Math
import heapq as heap
import sys
import copy

ROWS=5
COLS=5

def printable_board(board):
    return [ ('%3d ')*COLS  % board[j:(j+COLS)] for j in range(0, ROWS*COLS, COLS) ]

'''
Below functions move_right, move_left, rotate_right, rotate_left, move_clockwise, move_cclockwise, transpose_board are helper functions to get successor moves.
I reused the code from test file
'''
def move_right(state, row):
  state[row] = state[row][-1:] + state[row][:-1]
  return state

def move_left(board, row):
  board[row] = board[row][1:] + board[row][:1]
  return board

def rotate_right(board,row,residual):
    board[row] = [board[row][0]] +[residual] + board[row][1:]
    residual=board[row].pop()
    return residual

def rotate_left(board,row,residual):
    board[row] = board[row][:-1] + [residual] + [board[row][-1]]
    residual=board[row].pop(0)
    return residual

def move_clockwise(board):
    board[0]=[board[1][0]]+board[0]
    residual=board[0].pop()
    board=transpose_board(board)
    residual=rotate_right(board,-1,residual)
    board=transpose_board(board)
    residual=rotate_left(board,-1,residual)
    board=transpose_board(board)
    residual=rotate_left(board,0,residual)
    board=transpose_board(board)
    return board

def move_cclockwise(board):
    board[0]=board[0]+[board[1][-1]]
    residual=board[0].pop(0)
    board=transpose_board(board)
    residual=rotate_right(board,0,residual)
    board=transpose_board(board)
    residual=rotate_right(board,-1,residual)
    board=transpose_board(board)
    residual=rotate_left(board,-1,residual)
    board=transpose_board(board)
    return board

def transpose_board(board):
  return [list(col) for col in zip(*board)]


# return a list of possible successor states
def successors(state):
    moves=[]
    for i in range(ROWS):
        moves.append(['R'+str(i+1),move_right(copy.deepcopy(state), i)])

    for i in range(ROWS):
        moves.append(['L'+str(i+1),move_left(copy.deepcopy(state), i)])

    for i in range(COLS):
        moves.append(['U'+str(i+1),transpose_board(move_left(transpose_board(copy.deepcopy(state)), i))])

    for i in range(COLS):
        moves.append(['D'+str(i+1),transpose_board(move_right(transpose_board(copy.deepcopy(state)), i))])

    moves.append(['Oc',move_clockwise(copy.deepcopy(state))])
    
    moves.append(['Occ',move_cclockwise(copy.deepcopy(state))])
    
    
    state_Ic=np.array(copy.deepcopy(state))
    inner_state=state_Ic[1:-1,1:-1].tolist()
    inner_state = move_clockwise(inner_state)
    state_Ic[1:-1,1:-1]=np.array(inner_state)
    state_Ic=state_Ic.tolist()
    moves.append(['Ic',state_Ic])

    state_Icc=np.array(copy.deepcopy(state))
    inner_state=state_Icc[1:-1,1:-1].tolist()
    inner_state = move_cclockwise(inner_state)
    state_Icc[1:-1,1:-1]=np.array(inner_state)
    state_Icc=state_Icc.tolist()
    moves.append(['Icc',state_Icc])

    return moves
        
'''
heuristic function that I considered is the manhattan distance 
'''
def heuristic(state):
    d=0
    goalstate_indicies={1:[0,0],2:[0,1],3:[0,2],4:[0,3],5:[0,4],6:[1,0],7:[1,1],8:[1,2],9:[1,3],10:[1,4],11:[2,0],12:[2,1],13:[2,2],14:[2,3],15:[2,4],16:[3,0],17:[3,1],18:[3,2],19:[3,3],20:[3,4],21:[4,0],22:[4,1],23:[4,2],24:[4,3],25:[4,4]}
    for i in range(5):
        for j in range(5):
            x1,y1 = i,j #position in the current state
            x2,y2 = goalstate_indicies[state[i][j]] #position in the goal state
            d += Math.fabs(x1-x2) + Math.fabs(y1-y2)
    return d

# check if we've reached the goal
def is_goal(state):
    count=1
    gstate=[[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15], [16, 17, 18, 19, 20], [21, 22, 23, 24, 25]]
    for i in range(ROWS):
        for j in range(COLS):
            if gstate[i][j]!=state[i][j]:
                return False
    return True


def solve(initial_board):
    """
    solve method implements A* algorithm.
    """
    state=[]
    k=0
    for i in range(ROWS):
        temp=[]
        for j in range(COLS):
            temp.append(initial_board[k])
            k+=1
        state.append(temp)
    initial_board=state
    fringe=[] # the next node to be exlored
    fringe.append((9999,0,initial_board,[]))
    heap.heapify(fringe) # using heap data structure so that we will always have the next node to be explored in fringe at top
    while len(fringe)>0:
        (f,c,state,p)=heap.heappop(fringe) # f=heuristice(state)+c, c is the cost from initial board to the current state
        if is_goal(state):
            print(" goal found")
            return p
        moves=successors(state)
        for s in moves:
            heap.heappush(fringe,(heuristic(s[1])+c,c+1,s[1],p+[s[0]]))
    return [""]

# Please don't modify anything below this line
#
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a board filename"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]

    if len(start_state) != ROWS*COLS:
        raise(Exception("Error: couldn't parse start state file"))

    print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))

    print("Solving...")
    route = solve(tuple(start_state))
    
    print("Solution found in " + str(len(route)) + " moves:" + "\n" + " ".join(route))
