# cbachhu-admhaske-dpujari-a1
## Assignment 1

### Part 1: Birds, heuristics, and A
**Assigned member: Aditya Sanjay Mhaske**

Initial State: N=5

Goal State: Goal state is given

Stated Question:
On a power line sit five birds, each wearing a different number from 1 to N. They start in a random order and their goal is to re-arrange themselves to be in order from 1 to N (e.g., 12345), in as few steps as possible. In any one step, exactly one bird can exchange places with exactly one of its neighboring birds. We can pose this as a search problem in which there is a set of states S corresponding to all possible permutations of the birds

Successor Function: 
description of possible actions, a set of operators. It is a transformation function on a state representation, which convert it into another state. The successor function defines a relation of accessibility among states.

Heuristic Function:
The heuristic function is a way to inform the search about the direction to a goal. It provides an informed way to guess which neighbor of a node will lead to a goal. There is nothing magical about a heuristic function. It must use only information that can be readily obtained about a node.
Here Heuristic cost value calculated by counting total number of missing birds

Reference: Disccuesed with Dhanush Bharat Raj


### Part  2:  The  2022  Puzzle
**Assigned member: Chandra Kiran Bachhu**

Initial State:
We are given a board with 25 tiles (5*5)

Goal State:
Goal state is also given

Valid Moves:
Here, in single move instead of moving one tile 
-> an entire row is move right or left with right-most or left most is wrapped around to the other side
-> an entire column is move up or down with top-most or bottom-most is wrapped around to the other side
-> rotating the outer ring of tiles either clockwise or counterclockwise
-> rotating the inner ring of tiles either clockwise or counterclockwise
There shouldn't be any empty tile

Successor Function:
Successor function finds all possible moves from the current state. Possible moves as mentioned above in valid moves will result in 5(moves_right)+5(moves_left)+5(moves_up)+5(moves_down)+2(outer_ring_C&CC)+2(inner_ring_C&CC)=24. So each time a successor function is called it return 24 moves.

Approach

Used A* algorithm to solve this puzzle. Heuristic function h(s) is the sum of manhattan ditances (distance between a position of tile in the current state and position where it is supposed to be as in	 goal state). Fringe is implemented using heap data structure. Everytime insteaf of exploring all nodes in fringe only the top one(one with less f(s) = (h(s)+g(s)), g(s)=cost of moves to get current state from initial). 

The code works for board0 and for board1 it doesn't statisfy the time complexity.

Q) what is the branching factor of the search tree?
A) The branching factor is 24. Everytime a node is explored in fringe the successor function returns 24 moves.

Q) If the solution can be reached in 7 moves, about how many states would we need to explore before we found it if we used BFS instead of A* search? 
A) In A* we will explore 24n states (n=moves), in BFS we will explore 24^n states. Answer would be approximately 4586471424.

TERMINAL OUTPUT :
![image](https://media.github.iu.edu/user/21646/files/63631f96-98a0-487c-aa54-a76f5abc1215)

### Part 3: Road Trip
**Assigned member: Deveshwari Pujari**

State Space:
All possible routes from point ‘A’ to point ‘B’ covering all the essential cities exhaustively on the map.

Successor Function:
At any particular point/stop returns the collection of cities or nodes that are directly connected to it.

Edge Weights:
Minimize the corresponding parameters for our desired route based on the cost function's input- 1)time, 2)segments, 3)distance, 4)delivery 5)statetour 

Goal State:
The end node or the final destination of our desired route.

Heuristic Function:
Haversine distance is the selected heuristic function for this problem statement. This is an admissible heuristic function because it takes the cities' latitude and longitude into account. Therefore, the distance between two cities can be determined by drawing a straight line on the earth's surface, but it will always be less than the real distance of the path between them (the heuristic function never overestimates)

Search Algorithm:
The search algorithm used for this problem statement is A* search. A* Search Algorithm is a simple and efficient search algorithm that can be used to find the optimal path between two nodes in a graph. This technique always returns the optimal solution. As we use a priority queue based on a weighted combination of the heuristic function and the cost function f(n) can be denoted as : f(n) = g(n) + h(n), 
where :g(n) = cost of traversing from one node to another. This will vary from node to node, 
h(n) = heuristic approximation of the node's value.

Terminal Output:![Output](https://media.github.iu.edu/user/21510/files/3d49e2a7-4de0-489f-adbe-70afefa3f71e)
Pytest on Silo:![silo-op](https://media.github.iu.edu/user/21510/files/14a9d2d4-b4f9-4d7c-ba15-cd919e8b0d3c)


