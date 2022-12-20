

#!/usr/bin/env python3
import sys
from queue import PriorityQueue

N=5

# Initial state:

# Goal state:

def point(st):
    return st == list(range(1, N+1))

def point_position():
    return list(range(1,N+1))

# Successor function:

def increment(st):
    return [ st[0:n] + [st[n+1],] + [st[n],] + st[n+2:] for n in range(0, N-1) ]

def point_position_ch(element):
    goal = point_position()
    for i in range(len(goal)):
        if(element == goal[i]):
            return i
           
    return -1

def h(st):
    h_val = 0
    for i in range(len(st)):
        
        
        #Method used to calculated the misplaced birds count using hestoric value
        h_val += (abs(i - point_position_ch(st[i])))
           
    return h_val


#########
#Used BFS to solve this general equation
#
def solve(ini_st):
    frg =  PriorityQueue()
    frg.put((0, ini_st, []))
    while frg:
        (heuristic, st, path) = frg.get()
        if point(st):
            return path+[st,]
        for s in increment(st):
            frg.put((h(s), s, path+[st,]))

    return []


#Given code for error call and success function recall
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a test case filename"))

    t_count = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            t_count.append([ int(i) for i in line.split() ])
    for ini_st in t_count:
        print('From state ' + str(ini_st) + " found goal state by taking path: " + str(solve(ini_st)))
