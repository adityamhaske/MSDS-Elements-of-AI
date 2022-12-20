#
# raichu.py : Play the game of Raichu
#
# basrini-rdhonuks-admhaske!
#
# Based on skeleton code by D. Crandall, Oct 2021
#
import sys
from copy import deepcopy as dc
global Deb
DEBUG = False
def ChoosePiece(board,N,vertInd,HorInd):
    piece = board[vertInd][HorInd]
    if piece in 'wb':
        return successor_pichu(board,N,vertInd,HorInd)
    elif piece in 'WB':
        return successor_pika(board,N,vertInd,HorInd)
    elif piece in '@$':
        return successor_raichu(board,N,vertInd,HorInd)
    
def successor_pichu(board,N,vertInd,HorInd):

    AllIStates = list()
    # Moves for the white
    if board[vertInd][HorInd] == 'w':
        w_flag = True
        pichu_movset = [(1,-1,2,-2),(1,1,2,2)]
    elif  board[vertInd][HorInd] == 'b':
        w_flag  = False
        pichu_movset = [(-1,1,-2,2),(-1,-1,-2,-2)]
        
    for move in pichu_movset:  
        InterState = None
        if EdgeDet(vertInd+move[0],HorInd+move[1],N):
            if board[vertInd+move[0]][HorInd+move[1]] == '.':
                InterState = dc(board)
                InterState[vertInd+move[0]][HorInd+move[1]] = ('w' if w_flag else 'b')
                if vertInd+move[0] == N-1: InterState[vertInd+move[0]][HorInd+move[1]] = ('@' if w_flag else '$')
                InterState[vertInd][HorInd] = '.'
            elif board[vertInd+move[0]][HorInd+move[1]] == ('b' if w_flag else 'w') and EdgeDet(vertInd+move[2],HorInd+move[3],N) and board[vertInd+move[2]][HorInd+move[3]] == '.' :
                InterState = dc(board)
                InterState[vertInd+move[2]][HorInd+move[3]] = ('w' if w_flag else 'b')
                if vertInd+move[2] == N-1: InterState[vertInd+move[2]][HorInd+move[3]] = ('@' if w_flag else '$')
                InterState[vertInd][HorInd],InterState[vertInd+move[0]][HorInd+move[1]] = '.','.'
        
        if InterState: AllIStates += [InterState]

    return AllIStates

def successor_pika(board,N,vertInd,HorInd):

    AllIStates = list()
    Deb = []
    #Moves based on (row,row+1,row+2,col,col+1,col+2) and in order for left right and Forward(direction based on flag)
    if board[vertInd][HorInd] == 'W':
        w_flag = True
        pika_pmovset = [(0,0,0,-1,-2,-3),(0,0,0,1,2,3),(1,2,3,0,0,0)]
    elif  board[vertInd][HorInd] == 'B':
        w_flag = False
        pika_pmovset = [(0,0,0,-1,-2,-3),(0,0,0,1,2,3),(-1,-2,-3,0,0,0)]

    InterState = None
    
    for i,move in enumerate(pika_pmovset):
        if EdgeDet(vertInd+move[0],HorInd+move[3],N):
            if board[vertInd+move[0]][HorInd+move[3]]=='.':
                InterState = dc(board)
                InterState[vertInd+move[0]][HorInd+move[3]] = ('W' if w_flag else 'B')
                if i == 2 and vertInd+move[0] == (N-1 if w_flag else 0 ):InterState[vertInd+move[0]][HorInd] = ('@' if w_flag else '$')
                InterState[vertInd][HorInd] = '.'
                AllIStates += [InterState]
                
            elif board[vertInd+move[0]][HorInd+move[3]] in ('Bb' if w_flag else 'Ww') and EdgeDet(vertInd+move[1],HorInd+move[4],N) and board[vertInd+move[1]][HorInd+move[4]] == '.':
                InterState = dc(board)
                InterState[vertInd+move[1]][HorInd+move[4]] = ('W' if w_flag else 'B')
                if i == 2 and vertInd+move[1] == (N-1 if w_flag else 0 ):InterState[vertInd+move[1]][HorInd] = ('@' if w_flag else '$')
                InterState[vertInd][HorInd],InterState[vertInd+move[0]][HorInd+move[3]] = '.','.'
                Deb += InterState[vertInd+move[1]][HorInd]
                AllIStates += [InterState]
                
            if EdgeDet(vertInd+move[1],HorInd+move[4],N):
                if board[vertInd+move[1]][HorInd+move[4]] == '.' and board[vertInd+move[0]][HorInd+move[3]] == '.':
                    InterState = dc(board)
                    InterState[vertInd+move[1]][HorInd+move[4]] = 'W' if w_flag else 'B'
                    if i == 2 and vertInd+move[1] == (N-1 if w_flag else 0 ):InterState[vertInd+move[1]][HorInd] = ('@' if w_flag else '$')
                    InterState[vertInd][HorInd] = '.'
                    Deb += InterState[vertInd+move[1]][HorInd]
                    AllIStates += [InterState]

                elif board[vertInd+move[1]][HorInd+move[4]] in ('Bb' if w_flag else 'Ww') and board[vertInd+move[0]][HorInd+move[3]] == '.' and EdgeDet(vertInd+move[2],HorInd+move[5],N) and board[vertInd+move[2]][HorInd+move[5]] == '.':
                    InterState = dc(board)
                    InterState[vertInd+move[2]][HorInd+move[5]] = ('W' if w_flag else 'B')
                    if i == 2 and vertInd+move[2] == (N-1 if w_flag else 0 ):InterState[vertInd+move[2]][HorInd] = ('@' if w_flag else '$')
                    InterState[vertInd][HorInd],InterState[vertInd+move[1]][HorInd+move[4]] = '.','.'
                    Deb += InterState[vertInd+move[2]][HorInd]
                    AllIStates += [InterState] 
           
    return AllIStates    

def successor_raichu(board,N,vertInd,HorInd):

    linear_directions = [(-1,+0),(+1,+0),(+0,+1),(+0,-1)]
    #for i,dire in enumerate(linear_directions):
    if board[vertInd][HorInd] == '@':
        w_flag = True
        InterState = None
    elif board[vertInd][HorInd] == '$':
        w_flag = True
        InterState = None
    AllIStates = list()
    global Deb
    #Moves left
    for nexInd in range(1,N):
        if EdgeDet(vertInd,HorInd-nexInd,N):
            if board[vertInd][HorInd-nexInd]=='.':
                InterState = dc(board)
                InterState[vertInd][HorInd-nexInd],InterState[vertInd][HorInd] = ('@' if w_flag else '$'),'.'
                AllIStates+= [InterState]
            elif board[vertInd][HorInd-nexInd] in ('Ww@' if w_flag else 'Bb$'):break
            elif board[vertInd][HorInd-nexInd] in ('Bb$' if w_flag else 'Ww@'):
                for postInd in range(HorInd-nexInd-1,-1,-1):
                    if EdgeDet(vertInd,postInd,N) and board[vertInd][postInd] == '.' :
                        InterState = dc(board) 
                        InterState[vertInd][postInd],InterState[vertInd][HorInd],InterState[vertInd][HorInd-nexInd] = ('@' if w_flag else '$'),'.','.'
                        Deb += InterState[vertInd][postInd]
                        AllIStates+= [InterState]
                    elif EdgeDet(vertInd,postInd,N) and board[vertInd][postInd]!= '.' :break
                break
            linear_directions = [(-1,+0),(+1,+0),(+0,+1),(+0,-1)]
    #Moves Right
    for nexInd in range(1,N):
        if EdgeDet(vertInd,HorInd+nexInd,N):
            if board[vertInd][HorInd+nexInd]=='.':
                InterState = dc(board)
                InterState[vertInd][HorInd+nexInd],InterState[vertInd][HorInd] = ('@' if w_flag else '$'),'.'
                AllIStates+= [InterState]
            elif board[vertInd][HorInd+nexInd] in ('Ww@' if w_flag else 'Bb$'):break
            elif board[vertInd][HorInd+nexInd] in ('Bb$' if w_flag else 'Ww@'):
                for postInd in range(HorInd+nexInd+1,N):
                    if EdgeDet(vertInd,postInd,N) and board[vertInd][postInd] == '.' :
                        InterState = dc(board) 
                        InterState[vertInd][postInd] = ('@' if w_flag else '$')
                        InterState[vertInd][HorInd],InterState[vertInd][HorInd+nexInd] = '.','.'
                        Deb += InterState[vertInd][postInd]
                        AllIStates+= [InterState]
                    elif EdgeDet(vertInd,postInd,N) and board[vertInd][postInd]!= '.' : break
                break
    #Moves Bot
    for nexInd in range(1,N):
        if EdgeDet(vertInd+nexInd,HorInd,N):
            if board[vertInd+nexInd][HorInd]=='.':
                InterState = dc(board)
                InterState[vertInd+nexInd][HorInd],InterState[vertInd][HorInd] = ('@' if w_flag else '$'),'.'
                Deb += InterState[vertInd+nexInd][HorInd]
                AllIStates+= [InterState]
            elif board[vertInd+nexInd][HorInd] in ('Ww@' if w_flag else 'Bb$'): break
            elif board[vertInd+nexInd][HorInd] in ('Bb$' if w_flag else 'Ww@'):
                for postInd in range(vertInd+nexInd+1,N):
                    if EdgeDet(postInd,HorInd,N) and board[postInd][HorInd] == '.' :
                        InterState = dc(board)
                        InterState[postInd][HorInd] = ('@' if w_flag else '$')
                        InterState[vertInd][HorInd],InterState[vertInd+nexInd][HorInd] = '.','.'
                        Deb += InterState[postInd][HorInd]
                        AllIStates+= [InterState]
                    elif EdgeDet(postInd,HorInd,N) and board[postInd][HorInd]!= '.' :break
                break
    #Moves Top
    for nexInd in range(1,N):
        if EdgeDet(vertInd-nexInd,HorInd,N):
            if board[vertInd-nexInd][HorInd]=='.':
                InterState = dc(board)
                InterState[vertInd-nexInd][HorInd],InterState[vertInd][HorInd] = ('@' if w_flag else '$'),'.'
                AllIStates+= [InterState]
                Deb += InterState[vertInd-nexInd][HorInd]
            elif board[vertInd-nexInd][HorInd] in ('Ww@' if w_flag else 'Bb$'):break    
            elif board[vertInd-nexInd][HorInd] in ('Bb$' if w_flag else 'Ww@'):
                for postInd in range(vertInd-nexInd-1,-1,-1):
                    if EdgeDet(postInd,HorInd,N) and board[postInd][HorInd] == '.' :
                        InterState = dc(board)
                        InterState[postInd][HorInd],InterState[vertInd][HorInd],InterState[vertInd-nexInd][HorInd] = ('@' if w_flag else '$'),'.','.'
                        AllIStates+= [InterState]
                        Deb += InterState[postInd][HorInd]
                    elif EdgeDet(postInd,HorInd,N) and board[postInd][HorInd]!= '.' :break
                break
    dirt = [(-1,-1),(+1,+1),(-1,+1),(+1,-1)]
    #for i,dire in enumerate(diag_directions):
    #Moves BOT RIGHT
    for nexInd in range(1,N):
        if EdgeDet(vertInd+nexInd,HorInd+nexInd,N):
            if board[vertInd+nexInd][HorInd+nexInd]=='.':
                InterState = dc(board)
                InterState[vertInd+nexInd][HorInd+nexInd],InterState[vertInd][HorInd] = ('@' if w_flag else '$'),'.'
                Deb +=InterState[vertInd+nexInd][HorInd+nexInd]
                AllIStates += [InterState]
            elif board[vertInd+nexInd][HorInd+nexInd] in ('Ww@' if w_flag else 'Bb$'):break
            elif board[vertInd+nexInd][HorInd+nexInd] in ('Bb$' if w_flag else 'Ww@'):
                for postInd in range(1,N):
                    if EdgeDet(vertInd+(nexInd+postInd),HorInd+(nexInd+postInd),N) and board[vertInd+(nexInd+postInd)][HorInd+(nexInd+postInd)] == '.' :
                        InterState = dc(board)
                        InterState[vertInd+(nexInd+postInd)][HorInd+(nexInd+postInd)],InterState[vertInd][HorInd],InterState[vertInd+nexInd][HorInd+nexInd] = ('@' if w_flag else '$'),'.','.'
                        Deb += InterState[vertInd+(nexInd+postInd)][HorInd+(nexInd+postInd)]
                        AllIStates += [InterState]
                    elif EdgeDet(vertInd+(nexInd+postInd),HorInd+(nexInd+postInd),N) and board[vertInd+(nexInd+postInd)][HorInd+(nexInd+postInd)] != '.' : break
                break
    #Moves Top RIGHT
    for nexInd in range(1,N):
        if EdgeDet(vertInd-nexInd,HorInd+nexInd,N):
            if board[vertInd-nexInd][HorInd+nexInd]=='.':
                InterState = dc(board)
                InterState[vertInd-nexInd][HorInd+nexInd],InterState[vertInd][HorInd] = ('@' if w_flag else '$'),'.'
                AllIStates += [InterState]
            
            elif board[vertInd-nexInd][HorInd+nexInd] in ('Ww@' if w_flag else 'Bb$'): break
            elif board[vertInd-nexInd][HorInd+nexInd] in ('Bb$' if w_flag else 'Ww@'):
                for postInd in range(1,N):
                    if EdgeDet(vertInd-(nexInd+postInd),HorInd+(nexInd+postInd),N) and board[vertInd-(nexInd+postInd)][HorInd+(nexInd+postInd)] == '.':
                        InterState = dc(board)
                        InterState[vertInd-(nexInd+postInd)][HorInd+(nexInd+postInd)],InterState[vertInd][HorInd],InterState[vertInd-nexInd][HorInd+nexInd] = ('@' if w_flag else '$'),'.','.'
                        Deb += InterState[vertInd-(nexInd+postInd)][HorInd+(nexInd+postInd)]
                        AllIStates += [InterState]
                    elif EdgeDet(vertInd-(nexInd+postInd),HorInd+(nexInd+postInd),N) and board[vertInd-(nexInd+postInd)][HorInd+(nexInd+postInd)] != '.':break
                break
    #Moves BOT Left
    for nexInd in range(1,N):
        if EdgeDet(vertInd+nexInd,HorInd-nexInd,N):
            if board[vertInd+nexInd][HorInd-nexInd]=='.':
                InterState = dc(board)
                InterState[vertInd+nexInd][HorInd-nexInd],InterState[vertInd][HorInd] = ('@' if w_flag else '$'),'.'
                Deb += InterState[vertInd+nexInd][HorInd-nexInd]
                AllIStates += [InterState]
            elif board[vertInd+nexInd][HorInd-nexInd] in ('Ww@' if w_flag else 'Bb$'):break
            elif board[vertInd+nexInd][HorInd-nexInd] in ('Bb$' if w_flag else 'Ww@'):
                for postInd in range(1, N):
                    if EdgeDet(vertInd+(nexInd+postInd),HorInd-(nexInd+postInd),N) and board[vertInd+(nexInd+postInd)][HorInd-(nexInd+postInd)] == '.' :
                        InterState = dc(board)
                        InterState[vertInd+(nexInd+postInd)][HorInd-(nexInd+postInd)],InterState[vertInd][HorInd],InterState[vertInd+nexInd][HorInd-nexInd] = ('@' if w_flag else '$'),'.','.'
                        Deb= InterState[vertInd+(nexInd+postInd)][HorInd-(nexInd+postInd)]
                        AllIStates += [InterState]
                    elif EdgeDet(vertInd+(nexInd+postInd),HorInd-(nexInd+postInd),N) and board[vertInd+(nexInd+postInd)][HorInd-(nexInd+postInd)] != '.' :break
                break
    #Moves Top Left
    for nexInd in range(1,N):
        if EdgeDet(vertInd-nexInd,HorInd-nexInd,N):
            if board[vertInd-nexInd][HorInd-nexInd]=='.':
                InterState = dc(board)
                InterState[vertInd-nexInd][HorInd-nexInd],InterState[vertInd][HorInd] = ('@' if w_flag else '$'),'.'
                Deb += InterState[vertInd-nexInd][HorInd-nexInd]
                AllIStates += [InterState]
            elif board[vertInd-nexInd][HorInd-nexInd] in ('Ww@' if w_flag else 'Bb$'):break  
            elif board[vertInd-nexInd][HorInd-nexInd] in ('Bb$' if w_flag else 'Ww@'): 
                for postInd in range(1,N):
                    if EdgeDet(vertInd-(nexInd+postInd),HorInd-(nexInd+postInd),N) and board[vertInd-(nexInd+postInd)][HorInd-(nexInd+postInd)] == '.' :
                        InterState = dc(board)
                        InterState[vertInd-(nexInd+postInd)][HorInd-(nexInd+postInd)],InterState[vertInd][HorInd],InterState[vertInd-nexInd][HorInd-nexInd] = ('@' if w_flag else '$'),'.','.'
                        Deb += InterState[vertInd-(nexInd+postInd)][HorInd-(nexInd+postInd)]
                        AllIStates += [InterState]
                    elif EdgeDet(vertInd-(nexInd+postInd),HorInd-(nexInd+postInd),N) and board[vertInd-(nexInd+postInd)][HorInd-(nexInd+postInd)] != '.' :break
                break
    if DEBUG: return AllIStates,Deb
    return AllIStates 
  
def board_to_string(board, N):
    return "\n".join(board[i:i+N] for i in range(0, len(board), N))

def BEval(board,N,vertInd,HorInd):

    if board[vertInd][HorInd] in 'Ww@':
        w_flag =True
    elif board[vertInd][HorInd] in 'Bb$':
        w_flag =False
        
    dirt = [(-1,-1),(+1,+1),(-1,+1),(+1,-1),(-1,+0),(+1,+0),(+0,+1),(+0,-1)]
    points = 0
    for direct in dirt:
        #print(f'new piece{board[vertInd+direct[0]][HorInd+direct[1]]}')
        if not EdgeDet(vertInd+direct[0],HorInd+direct[1],N):
            #print(f'not in vertInd{str(direct[0])} and HorInd{str(direct[1])}')
            points+=1
    if board[vertInd][HorInd] not in 'Ww@Bb$.':
        raise "corrupted piece"
    D=0
    for direct in dirt:
        D +=1
        if EdgeDet(vertInd+direct[0],HorInd+direct[1],N):
            if board[vertInd+direct[0]][HorInd+direct[1]] in ('Ww@'  if w_flag else 'Bb$'): points +=3 #print(f"for {D} - 1")
            elif board[vertInd+direct[0]][HorInd+direct[1]] in ('Bb$'  if w_flag else 'Ww@'): points -=1 #print(f"for {D} - 2")
            else:points += 0
    return points if w_flag else -points


    
def Eval2MinMax(board,N,p):
    points = 0
    piece_weights  = {'.':1,'w':11,'W':12,'@':15,'b':-11,'B':-12,'$':-15}
    for a in range(N):
        for b in range(N): 
            if board[a][b] != '.': points += BEval(board,N,a,b)
    for piece in Two2oneD(board):points +=piece_weights[piece]
    bstr = dict()
    Deb = "".join(Two2oneD(board))
    for pieces in Deb:
        if pieces != '.' and pieces not in bstr:bstr[pieces] =1
        elif  pieces != '.':bstr[pieces] +=1
        
    # if p == 'w':
    #     Dub = points*(1*(bstr.get('w',0)-bstr.get('b',0))  + 5* (bstr.get('W',0)-bstr.get('B',0))+ 3*(bstr.get('@',0)-bstr.get('$',0)))
    # else:
    #     Dub = points*(1*(bstr.get('b',0)-bstr.get('w',0))  + 5* (bstr.get('B',0)-bstr.get('W',0))+ 3*(bstr.get('$',0)-bstr.get('@',0)))
    
    return points

def EdgeDet(x,y,N):
    return True if (0<=x<N) and (0<=y<N) else False
    
def minimax(board,N,count,alpha,beta,player):
    # MiniMax implementation based on 'https://www.youtube.com/watch?v=l-hh51ncgDI&t'

    if count == 0 or Is_goal(board,N):return (Eval2MinMax(board,N,player),board)
    best = None
    maxEval = float('-inf')
    minEval = float('inf')
    if player == 'w':
        for a in range(N):
            for b in range(N):
                if board[a][b] in 'wW@' :
                    for UpInterState in ChoosePiece(board,N,a,b):
                        boardpoints,InterState = minimax(UpInterState,N,count-1,alpha,beta,'b')
                        if boardpoints > maxEval:best,maxEval = UpInterState,boardpoints
                        alpha = max(alpha,boardpoints)
                        if beta<= alpha:break
        return maxEval,best
    if player == 'b':
        for a in range(N):
            for b in range(N):
                if board[a][b] in 'bB$' :
                    for UpInterState in ChoosePiece(board,N,a,b):
                        boardpoints,InterState = minimax(UpInterState,N,count-1,alpha,beta,'w')
                        if boardpoints < minEval:best,minEval = UpInterState,boardpoints
                        beta = min(beta,boardpoints)
                        if beta <= alpha:break
        return minEval,best

def Is_goal(board,N):
    bstr = dict()
    Deb = "".join(Two2oneD(board))
    for pieces in Deb:
        if pieces != '.' and pieces not in bstr:bstr[pieces] =1
        elif  pieces != '.':bstr[pieces] +=1
    if len(bstr.keys())==3 and 'b' in bstr.keys():return True
    elif len(bstr.keys())==3 and 'w' in bstr.keys():return False

def visualizer(board,N):
    for i in range(N):print(board[i*N:(i+1)*N],end='\n')
        
        
def one2twoD(mov_space,N):
    lst = list()
    for i in range(N): 
        lst.append(mov_space[i*N:(i+1)*N])
    return lst

def Two2oneD(mov_space):
            return [j for i in mov_space for j in i]

def find_best_move(board, N, player, timelimit):
    for i in range(1000):
        score,res = minimax(one2twoD(list(board),N),N,i,float('-inf'),float('inf'),player)
        yield res


if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise Exception("Usage: Raichu.py N player board timelimit")
        
    (_, N, player, board, timelimit) = sys.argv
    N=int(N)
    timelimit=int(timelimit)
    if player not in "wb":
        raise Exception("Invalid player.")

    if len(board) != N*N or 0 in [c in "wb.WB@$" for c in board]:
        Deb = board
        raise Exception("Bad board string.")

    print("Searching for best move for " + player + " from board state: \n" + board_to_string(board,N))
    print("Here's what I decided:")
    for new_board in find_best_move(board, N, player, timelimit):
        print("".join(Two2oneD(new_board)))
        Deb = "".join(Two2oneD(new_board))
        #visualizer("".join(Two2oneD(new_board)),N)
