import time
import math
import os.path
from os import path

#CONSTANT NON CHANGING DATA
surround_B = [(1, 1, "SE"),(0, 1, "E"), (1, 0, "S"), (-1, 1, "NE"), (1, -1, "SW"), (-1, 0, "N"), (0, -1, "W"), (-1, -1, "NW")]
surround_W = [(-1, -1, "NW"),(-1, 0, "N"), (0, -1, "W"),(-1, 1, "NE"),(1, -1, "SW"),(0, 1, "E"),(1, 0, "S"),(1, 1, "SE")]
surround_B_awayfrom_camp = [(1, 1, "SE"),(0, 1, "E"), (1, 0, "S")]
surround_W_awayfrom_camp = [(-1, -1, "NW"),(-1, 0, "N"),(0, -1, "W")]

#DECLARING CAMPS, OPPONENTS AND THEIR LOCATIONS
B_CAMP = [[0,0],[0,1],[0,2],[0,3],[0,4],[1,0],[1,1],[1,2],[1,3],[1,4],[2,0],[2,1],[2,2],[2,3],[3,0],[3,1],[3,2],[4,0],[4,1]]
W_CAMP = [[15,15],[15,14],[15,13],[15,12],[15,11],[14,15],[14,14],[14,13],[14,12],[14,11],[13,15],[13,14],[13,13],[13,12],[12,15],[12,14],[12,13],[11,15],[11,14]]
no_B_CAMP = 19; no_W_CAMP = 19
no_B_in_B = 0;  no_B_in_W = 0
no_W_in_B = 0;  no_W_in_W = 0
B_in_B = [];    B_in_W = []
W_in_B = [];    W_in_W = []
B_pos = [];     W_pos = []
player_name = ''; opponent_name = ''
depth = 0
################################ PRINTING RESULT ################################

def printResult(type_of_move, path):
    
    i = 0
    len_path = len(path)
    while (i < len(path) - 1):
        if (i != len(path)-2):
            m = type_of_move + " " + str(path[i][1])+ ","+ str(path[i][0])+ " "+str(path[i+1][1])+ ","+ str(path[i+1][0]) + "\n"
            f.write(m)
        else:
            m = type_of_move + " " + str(path[i][1])+ ","+ str(path[i][0])+ " "+str(path[i+1][1])+ ","+ str(path[i+1][0])
            f.write(m)
        i += 1
def printBoard(status):
    #printing the board
    print("\n******************** status *********************\n")
    index_arr = ['0','1','2','3','4','5','6','7','8','9','0','1','2','3','4','5']
    print ("   ", end="")
    print (index_arr)
    for i in range (16):
        if (i < 10):    num = str(0) + str(i); print (num, board[i], num)
        else:           print (i, board[i],i)
    print ("   ", end=""); print (index_arr)
def pieceStats():
    print ("B_CAMP:",B_CAMP, "\n"); print ("W_CAMP:",W_CAMP, "\n")
    print ("no_B_CAMP:",no_B_CAMP, "\n"); print ("no_W_CAMP:",no_W_CAMP, "\n")
    print ("no_B_in_B:",no_B_in_B, "\n"); print ("no_B_in_W:",no_B_in_W, "\n")
    print ("no_W_in_B:",no_W_in_B, "\n"); print ("no_W_in_W:",no_W_in_W, "\n")
    print ("B_in_B:",B_in_B, "\n"); print ("B_in_W:",B_in_W, "\n")
    print ("W_in_B:",W_in_B, "\n"); print ("W_in_W:",W_in_W, "\n")
    print ("W_pos:",W_pos, "\n"); print ("B_pos:",B_pos, "\n")
#################################### REUSABLE E and J FUNCTIONS #######################################

###################################################################################### GAME PLAY ######################################################################################
def valid_moves(board, current_player):
    legal_moves = []        #Format is [('E', [(0,0),(1,1)]),('J', [(0,0),(1,1),(2,2),(3,3),(4,4)]) ]
    no_B_in_B = 0;  no_B_in_W = 0
    no_W_in_B = 0;  no_W_in_W = 0
    B_in_B = [];    B_in_W = []
    W_in_B = [];    W_in_W = []
    B_pos = [];     W_pos = []
    

    #DIAGONALTRAVERSE AND STORING Bs and Ws
    for k in range (0, 16):
        i = k; j = 0
        while (i >= 0):
            if (board[i][j] == 'W'):    W_pos.append([i,j])
            if (board[i][j] == 'B'):    B_pos.append([i,j])
            if ([i,j] in B_CAMP and board[i][j] == 'B'): no_B_in_B += 1; B_in_B.append([i,j])
            if ([i,j] in W_CAMP and board[i][j] == 'B'): no_B_in_W += 1; B_in_W.append([i,j])
            if ([i,j] in B_CAMP and board[i][j] == 'W'): no_W_in_B += 1; W_in_B.append([i,j])
            if ([i,j] in W_CAMP and board[i][j] == 'W'): no_W_in_W += 1; W_in_W.append([i,j])
            i -= 1; j += 1
            
    for k in range (1, 16):
        i = 15; j = k
        while (j <= 15):
            if (board[i][j] == 'W'):    W_pos.append([i,j])
            if (board[i][j] == 'B'):    B_pos.append([i,j])
            if ([i,j] in B_CAMP and board[i][j] == 'B'): no_B_in_B += 1; B_in_B.append([i,j])
            if ([i,j] in W_CAMP and board[i][j] == 'B'): no_B_in_W += 1; B_in_W.append([i,j])
            if ([i,j] in B_CAMP and board[i][j] == 'W'): no_W_in_B += 1; W_in_B.append([i,j])
            if ([i,j] in W_CAMP and board[i][j] == 'W'): no_W_in_W += 1; W_in_W.append([i,j])
            i -= 1; j += 1
    B_pos.reverse()
    B_in_B.reverse()
    B_in_W.reverse()

        
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Player - WHITE <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    if (current_player == "W"):
        #_________________________________________________________________________________________________________________________________
        #CONDITION 1: if at least one piece inside own camp
        # 1a) inside to outside camp (PUSHING OUT W FROM W's CAMP WHEN AT LEAST 1 W in W_CAMP)
        # 1b) within camp, if 1a is not possible (WHEN W in W_CAMP cannot move out, then move W inside W_CAMP further away from corner)
        #_________________________________________________________________________________________________________________________________
        
        if (no_W_in_W >0):
            
            ##Condition 1a)
            #E move
            for i,j in W_in_W:                                                          
                for dx, dy, name in surround_W:                                         
                    if (0<= i + dx <=15 and 0 <= j + dy <= 15):
                        if (board[i + dx][j + dy] == '.' and ([i + dx,j + dy] not in W_CAMP)): 
                                walking_path = [(i,j),(i+dx,j+dy)]
                                legal_moves.append(['E', walking_path])
            
            #J moves
            for i,j in W_in_W:
                path = [[[] for _ in range(16)] for _ in range(16)]
                q = []
                q.append((i,j))
                path[i][j] += [(i,j)]

                while (len(q) > 0):         #running condition - frontier cannot be empty
                    left, right = q.pop(0)
                    #children/possible further jumps
                    for dx, dy, name in surround_W:
                        if ((0<= left + dx <=15) and (0 <= right + dy <= 15) and (0<= left + 2*dx <=15) and (0 <= right + 2*dy <= 15) and (board[left + dx][right + dy] != '.') and (board[left + 2*dx][right + 2*dy] == '.')):
                            #below, add the condition that the node has not been visited : path[left+2*dx][right+2*dy] == []
                            if (path[left+2*dx][right+2*dy] == []):
                                q.append((left+(2*dx), right+(2*dy)))
                                path[left+2*dx][right+2*dy] = path[left][right] + [(left + 2*dx,right + 2*dy)]
                                if ([left+2*dx,right+2*dy] not in W_CAMP):
                                    legal_moves.append(['J', path[left+2*dx][right+2*dy]])
            if (len(legal_moves) > 0 ): return legal_moves
            
            ##Condition 1b)
            #E move
            for i,j in W_in_W:                                                          
                for dx, dy, name in surround_W_awayfrom_camp:                                         
                    if (0<= i + dx <=15 and 0 <= j + dy <= 15):
                        if (board[i + dx][j + dy] == '.' and ((i+dx < i) or (j + dy < j))): 
                                walking_path = [(i,j),(i+dx,j+dy)]
                                legal_moves.append(['E', walking_path])
            
            #J move
            for i,j in W_in_W:
                path = [[[] for _ in range(16)] for _ in range(16)]
                q = []
                q.append((i,j))
                path[i][j] += [(i,j)]

                while (len(q) > 0):         #running condition - frontier cannot be empty
                    left, right = q.pop(0)
                    #children/possible further jumps
                    for dx, dy, name in surround_W:
                        if ((0<= left + dx <=15) and (0 <= right + dy <= 15) and (0<= left + 2*dx <=15) and (0 <= right + 2*dy <= 15) and (board[left + dx][right + dy] != '.') and (board[left + 2*dx][right + 2*dy] == '.')):
                            #below, add the condition that the node has not been visited : path[left+2*dx][right+2*dy] == []
                            if (path[left+2*dx][right+2*dy] == []):
                                q.append((left+(2*dx), right+(2*dy)))
                                path[left+2*dx][right+2*dy] = path[left][right] + [(left + 2*dx,right + 2*dy)]
                                if (((left+(2*dx)) <= i) and ((right + (2*dy)) <= j)):  #i, j new change
                                    legal_moves.append(['J', path[left+2*dx][right+2*dy]])
            if (len(legal_moves) > 0 ): return legal_moves
        
            
        #__________________________________________________________________________________________________________________________________________________________________
        #CONDITION 2 and 3:
            #2: player cannot make a move that starts outside my camp and ends up inside my camp
            #3: once a piece has reached the opposing camp, a play cannot result in that piece leaving the camp (search space is only the W pieces in B_CAMP)
        #__________________________________________________________________________________________________________________________________________________________________
        #FOR CONDITION 2, search space is all W pieces not in either of the camps
        W_outside_camps = []
        for v in W_pos: W_outside_camps.append(v)
        for val in W_pos:
            if (val in W_in_B): W_outside_camps.remove(val)
        
        
        #Condition 2
        #E move
        if (len(W_outside_camps)>0):
            for i,j in W_outside_camps:
                    for dx, dy, name in surround_W:                                         
                        if (0<= i + dx <=15 and 0 <= j + dy <= 15):
                            if (board[i + dx][j + dy] == '.' and ([i + dx,j + dy] not in W_CAMP)): 
                                    walking_path = [(i,j),(i+dx,j+dy)]
                                    legal_moves.append(['E', walking_path])
        #Condition 2
        #J move
        if (len(W_outside_camps)>0):
            for i,j in W_outside_camps:
                path = [[[] for _ in range(16)] for _ in range(16)]
                q = []
                q.append((i,j))
                path[i][j] += [(i,j)]

                while (len(q) > 0):         #running condition - frontier cannot be empty
                    left, right = q.pop(0)
                    #children/possible further jumps
                    for dx, dy, name in surround_W:
                        if ((0<= left + dx <=15) and (0 <= right + dy <= 15) and (0<= left + 2*dx <=15) and (0 <= right + 2*dy <= 15) and (board[left + dx][right + dy] != '.') and (board[left + 2*dx][right + 2*dy] == '.')):
                            #below, add the condition that the node has not been visited : path[left+2*dx][right+2*dy] == []
                            if (path[left+2*dx][right+2*dy] == []):
                                q.append((left+(2*dx), right+(2*dy)))
                                path[left+2*dx][right+2*dy] = path[left][right] + [(left + 2*dx,right + 2*dy)]
                                if ([left+2*dx,right+2*dy] not in W_CAMP):
                                    legal_moves.append(['J', path[left+2*dx][right+2*dy]])
                                    
        #Condition 3
        #E move
        if (len(W_in_B) > 0):
            for i,j in W_in_B:                                                          
                    for dx, dy, name in surround_W:                                         
                        if (0<= i + dx <=15 and 0 <= j + dy <= 15):
                            if (board[i + dx][j + dy] == '.' and ([i + dx,j + dy] in B_CAMP)):
                                    walking_path = [(i,j),(i+dx,j+dy)]
                                    legal_moves.append(['E', walking_path])
        
        
            
        #Condition 3
        #J move
        if (len(W_in_B) > 0):
            for i,j in W_in_B:
                path = [[[] for _ in range(16)] for _ in range(16)]
                q = []
                q.append((i,j))
                path[i][j] += [(i,j)]

                while (len(q) > 0):         #running condition - frontier cannot be empty
                    left, right = q.pop(0)
                    #children/possible further jumps
                    for dx, dy, name in surround_W:
                        if ((0<= left + dx <=15) and (0 <= right + dy <= 15) and (0<= left + 2*dx <=15) and (0 <= right + 2*dy <= 15) and (board[left + dx][right + dy] != '.') and (board[left + 2*dx][right + 2*dy] == '.')):
                            #below, add the condition that the node has not been visited : path[left+2*dx][right+2*dy] == []
                            if (path[left+2*dx][right+2*dy] == []):
                                q.append((left+(2*dx), right+(2*dy)))
                                path[left+2*dx][right+2*dy] = path[left][right] + [(left + 2*dx,right + 2*dy)]
                                if ([left+2*dx,right+2*dy] in B_CAMP):
                                    legal_moves.append(['J', path[left+2*dx][right+2*dy]])
    if (len(legal_moves) > 0 ): return legal_moves
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Player - BLACK<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    if (current_player == "B"):
        #_________________________________________________________________________________________________________________________________
        #CONDITION 1: if at least one piece inside own camp
        # 1a) inside to outside camp (PUSHING OUT W FROM W's CAMP WHEN AT LEAST 1 W in W_CAMP)
        # 1b) within camp, if 1a is not possible (WHEN W in W_CAMP cannot move out, then move W inside W_CAMP further away from corner)
        #_________________________________________________________________________________________________________________________________
        if (no_B_in_B >0):
            
            ##Condition 1a)
            #E move
            for i,j in B_in_B:                                                          
                for dx, dy, name in surround_B:                                         
                    if (0<= i + dx <=15 and 0 <= j + dy <= 15):
                        if (board[i + dx][j + dy] == '.' and ([i + dx,j + dy] not in B_CAMP)): 
                                walking_path = [(i,j),(i+dx,j+dy)]
                                legal_moves.append(['E', walking_path])
            
            #J moves
            for i,j in B_in_B:
                path = [[[] for _ in range(16)] for _ in range(16)]
                q = []
                q.append((i,j))
                path[i][j] += [(i,j)]

                while (len(q) > 0):         #running condition - frontier cannot be empty
                    left, right = q.pop(0)
                    #children/possible further jumps
                    for dx, dy, name in surround_B:
                        if ((0<= left + dx <=15) and (0 <= right + dy <= 15) and (0<= left + 2*dx <=15) and (0 <= right + 2*dy <= 15) and (board[left + dx][right + dy] != '.') and (board[left + 2*dx][right + 2*dy] == '.')):
                            #below, add the condition that the node has not been visited : path[left+2*dx][right+2*dy] == []
                            if (path[left+2*dx][right+2*dy] == []):
                                q.append((left+(2*dx), right+(2*dy)))
                                path[left+2*dx][right+2*dy] = path[left][right] + [(left + 2*dx,right + 2*dy)]
                                if ([left+2*dx,right+2*dy] not in B_CAMP):
                                    legal_moves.append(['J', path[left+2*dx][right+2*dy]])
            if (len(legal_moves) > 0 ): return legal_moves
            
            ##Condition 1b)
            #E move
            for i,j in B_in_B:                                                          
                for dx, dy, name in surround_B_awayfrom_camp:                                         
                    if (0<= i + dx <=15 and 0 <= j + dy <= 15):
                        if (board[i + dx][j + dy] == '.' and ((i+dx > i) or (j + dy > j))): 
                                walking_path = [(i,j),(i+dx,j+dy)]
                                legal_moves.append(['E', walking_path])
            
            #J move
            for i,j in B_in_B:
                path = [[[] for _ in range(16)] for _ in range(16)]
                q = []
                q.append((i,j))
                path[i][j] += [(i,j)]

                while (len(q) > 0):         #running condition - frontier cannot be empty
                    left, right = q.pop(0)
                    #children/possible further jumps
                    for dx, dy, name in surround_B:
                        if ((0<= left + dx <=15) and (0 <= right + dy <= 15) and (0<= left + 2*dx <=15) and (0 <= right + 2*dy <= 15) and (board[left + dx][right + dy] != '.') and (board[left + 2*dx][right + 2*dy] == '.')):
                            #below, add the condition that the node has not been visited : path[left+2*dx][right+2*dy] == []
                            if (path[left+2*dx][right+2*dy] == []):
                                q.append((left+(2*dx), right+(2*dy)))
                                path[left+2*dx][right+2*dy] = path[left][right] + [(left + 2*dx,right + 2*dy)]
                                if (((left+(2*dx)) >= i) and ((right + (2*dy)) >= j)):  #i, j new change
                                    legal_moves.append(['J', path[left+2*dx][right+2*dy]])
            if (len(legal_moves) > 0 ): return legal_moves
        
            
        #__________________________________________________________________________________________________________________________________________________________________
        #CONDITION 2 and 3:
            #2: player cannot make a move that starts outside my camp and ends up inside my camp
            #3: once a piece has reached the opposing camp, a play cannot result in that piece leaving the camp (search space is only the W pieces in B_CAMP)
        #__________________________________________________________________________________________________________________________________________________________________
        #FOR CONDITION 2, search space is all W pieces not in either of the camps
        B_outside_camps = []
        for v in B_pos: B_outside_camps.append(v)
        for val in B_pos:
            if (val in B_in_W): B_outside_camps.remove(val)
        
        #Condition 2
        #E move
        if (len(B_outside_camps)>0):
            for i,j in B_outside_camps:                                                          
                    for dx, dy, name in surround_B:                                         
                        if (0<= i + dx <=15 and 0 <= j + dy <= 15):
                            if (board[i + dx][j + dy] == '.'  and ([i + dx,j + dy] not in B_CAMP)): 
                                    walking_path = [(i,j),(i+dx,j+dy)]
                                    legal_moves.append(['E', walking_path])
        #Condition 2
        #J move
        if (len(B_outside_camps)>0):
            for i,j in B_outside_camps:
                path = [[[] for _ in range(16)] for _ in range(16)]
                q = []
                q.append((i,j))
                path[i][j] += [(i,j)]

                while (len(q) > 0):         #running condition - frontier cannot be empty
                    left, right = q.pop(0)
                    #children/possible further jumps
                    for dx, dy, name in surround_B:
                        if ((0<= left + dx <=15) and (0 <= right + dy <= 15) and (0<= left + 2*dx <=15) and (0 <= right + 2*dy <= 15) and (board[left + dx][right + dy] != '.') and (board[left + 2*dx][right + 2*dy] == '.')):
                            #below, add the condition that the node has not been visited : path[left+2*dx][right+2*dy] == []
                            if (path[left+2*dx][right+2*dy] == []):
                                q.append((left+(2*dx), right+(2*dy)))
                                path[left+2*dx][right+2*dy] = path[left][right] + [(left + 2*dx,right + 2*dy)]
                                if ([left+2*dx,right+2*dy] not in B_CAMP):
                                    legal_moves.append(['J', path[left+2*dx][right+2*dy]])        

        #Condition 3
        #E move
        if (len(B_in_W) > 0):
            for i,j in B_in_W:                                                          
                    for dx, dy, name in surround_B:                                         
                        if (0<= i + dx <=15 and 0 <= j + dy <= 15):
                            if (board[i + dx][j + dy] == '.' and ([i + dx,j + dy] in W_CAMP)):
                                    walking_path = [(i,j),(i+dx,j+dy)]
                                    legal_moves.append(['E', walking_path])
        
        
            
        #Condition 3
        #J move
        if (len(B_in_W) > 0):
            for i,j in B_in_W:
                path = [[[] for _ in range(16)] for _ in range(16)]
                q = []
                q.append((i,j))
                path[i][j] += [(i,j)]

                while (len(q) > 0):         #running condition - frontier cannot be empty
                    left, right = q.pop(0)
                    #children/possible further jumps
                    for dx, dy, name in surround_B:
                        if ((0<= left + dx <=15) and (0 <= right + dy <= 15) and (0<= left + 2*dx <=15) and (0 <= right + 2*dy <= 15) and (board[left + dx][right + dy] != '.') and (board[left + 2*dx][right + 2*dy] == '.')):
                            #below, add the condition that the node has not been visited : path[left+2*dx][right+2*dy] == []
                            if (path[left+2*dx][right+2*dy] == []):
                                q.append((left+(2*dx), right+(2*dy)))
                                path[left+2*dx][right+2*dy] = path[left][right] + [(left + 2*dx,right + 2*dy)]
                                if ([left+2*dx,right+2*dy] in W_CAMP):
                                    legal_moves.append(['J', path[left+2*dx][right+2*dy]])
            
            
    return legal_moves

def win_detect(board):
    W_won = 1; B_won = 1   #assume white and black won - flags

    left_B = 0; left_point = 0
    for pos in B_CAMP:
        if board[pos[0]][pos[1]] == '.':
            left_point += 1
        if board[pos[0]][pos[1]] == 'B':
            left_B += 1
    
    right_W = 0; right_point = 0
    for pos in W_CAMP:
        if board[pos[0]][pos[1]] == '.':
            right_point += 1
        if board[pos[0]][pos[1]] == 'W':
            right_W += 1

    #if (board[13][15] == "W" and board[1][1] == "B"):      return "dummy_win"  #REMOVE
    if (left_point == 0 and left_B != 19):  return "W"
    elif (right_point == 0 and right_W != 19): return "B"
    else:               return "None"

def distance(pos1,pos2):
    return math.sqrt((pos2[0]-pos1[0])**2 + (pos2[1]-pos1[1])**2)
    
def utility(board):
    black = 0
    white = 0
    value = 0
    value1 = 0     #REMOVE
    value2 = 0      #REMOVE
    for i in range (16):
        for j in range(16):
            piece = board[i][j]

            if (piece == 'W'): 
                distList = [distance((i,j), goals) for goals in B_CAMP if board[goals[0]][goals[1]] != 'W']
                value1 -= max(distList) if len(distList) != 0   else - 100
                
            elif (piece == 'B'):
                distListt = [distance((i,j), goals) for goals in W_CAMP if board[goals[0]][goals[1]] != 'B']
                value2 += max(distListt) if len(distListt) != 0   else + 100
                
    value = value1 + value2
    if player_name == "B":
        value *= -1

    #if (player_name == 'W'):                    value = black/white
    #else:                                       value = white/black
    if (win_detect(board) == "W"):      return float('inf') #DOUBT #REMOVE
    elif (win_detect(board) == "B"):    return float('-inf')      #DOUBT
        
    return value
    
def min_value(board, depth, alpha, beta, start, timeLimit):   #return action
    end = time.time()
    minv = float('inf')
    min_path = None
    min_move_type = None
    

    #Termination condition
    if (win_detect(board) != "None" or depth <= 0 or (end - start >= 1.5)): # or (start - end < = timeLimit)
        evaluation = utility(board)
        return (evaluation,[min_move_type, min_path])

    #finding valid moves 
    actions = []
    actions = valid_moves(board, opponent_name)
    #iterating through each action
    if (len(actions)> 0):
        depth -= 1
        for move_type, path in actions:
            #implement the action - temporarily
            from_x = path[0][0]; from_y = path[0][1]; to_x = path[len(path) -1][0]; to_y = path[len(path) -1][1];
            board[to_x][to_y] = opponent_name; board[from_x][from_y] = '.'
            (m, [max_move_type, max_path]) = max_value(board, depth, alpha, beta, start, timeLimit)
            if m < minv:
                minv = m
                min_move_type = move_type
                min_path = path
            #setting back the pieces
            board[to_x][to_y] = '.'; board[from_x][from_y] = opponent_name
            
            #alpha beta condition
            if (minv <= alpha): return (minv, [min_move_type, min_path])
            beta = min(beta, minv)
            
    return (minv, [min_move_type, min_path])

def max_value(board, depth, alpha, beta, start, timeLimit):
    end = time.time()
    maxv = float('-inf')
    max_path = None
    max_move_type = None
    
    #Termination condition
    if (win_detect(board) != "None" or depth <= 0 or (end - start  >= 1.5)):
        evaluation = utility(board)
        return (evaluation, [max_move_type,max_path])

    #finding valid moves 
    actions = []
    actions = valid_moves(board, player_name)
    #iterating through each action
    if (len(actions)> 0):
        depth -= 1
        for move_type, path in actions: 
            #implement the action - temporarily
            from_x = path[0][0]; from_y = path[0][1]; to_x = path[len(path) -1][0]; to_y = path[len(path) -1][1];
            board[to_x][to_y] = player_name; board[from_x][from_y] = '.'
            (m, [min_move_type, min_path]) = min_value(board, depth, alpha, beta, start, timeLimit) 
            if m > maxv:
                maxv = m
                max_path = path
                max_move_type = move_type
            #setting back the pieces
            board[to_x][to_y] = '.'; board[from_x][from_y] = player_name

            #alpha beta condition
            if (maxv >= beta): return (maxv, [max_move_type,max_path])
            alpha = max(alpha, maxv)
                
    return (maxv, [max_move_type,max_path])

def game(board, player_name, remaining_time, timeLimit):
    start = time.time()
    alpha = float('-inf'); beta = float('inf')
    (m, path) = max_value(board, depth, alpha, beta, start, timeLimit)  #return type has to be a list like ['J/E', [(0,0),(1,1),(4,5),(7,8)]]
    end = time.time()
    #print ("TIME TAKEN: ", end-start)    
    return path
###################################################################################### SINGLE PLAY ######################################################################################
def single_E_move_W(search_space, surround, condition):
    for i,j in search_space:                                                          #for each of the 19 pieces
                for dx, dy, name in surround:                                         #each surrounding
                    if (0<= i + dx <=15 and 0 <= j + dy <= 15):                         #check if inside matrix
                        #condition 1 - when pieces inside camp
                        #1a) inside to outside camp 
                        if (condition == "condition1a"):
                            if (board[i + dx][j + dy] == '.' and ([i + dx,j + dy] not in W_CAMP)): 
                                walking_path = [(i,j),(i+dx,j+dy)]
                                return ['E', walking_path]
                        #1b) within camp
                        if (condition == "condition1b"):
                            if (board[i + dx][j + dy] == '.' and ((i+dx < i) or (j + dy < j))): 
                                walking_path = [(i,j),(i+dx,j+dy)]
                                return ['E', walking_path]
                        #condition 2 = not in any camp
                        if (condition == "condition2"):
                            if (board[i + dx][j + dy] == '.' and ([i + dx,j + dy] not in W_CAMP)): 
                                walking_path = [(i,j),(i+dx,j+dy)]
                                return ['E', walking_path]
                        #condition 3 - inside opponent's camp
                        if (condition == "condition3"):
                            if (board[i + dx][j + dy] == '.' and ([i + dx,j + dy] in B_CAMP)): 
                                walking_path = [(i,j),(i+dx,j+dy)]
                                return ['E', walking_path]
                            
def single_J_move_W(search_space, surround, condition):
    for i,j in search_space:
        path = [[[] for _ in range(16)] for _ in range(16)]
        q = []
        q.append((i,j))
        path[i][j] += [(i,j)]

        while (len(q) > 0):         #running condition - frontier cannot be empty
            left, right = q.pop(0)
            #children/possible further jumps
            for dx, dy, name in surround:
                if ((0<= left + dx <=15) and (0 <= right + dy <= 15) and (0<= left + 2*dx <=15) and (0 <= right + 2*dy <= 15) and (board[left + dx][right + dy] != '.') and (board[left + 2*dx][right + 2*dy] == '.')):
                    #condition 1a or condition 2
                    if (condition == "condition1a" or condition == "condition2" ):
                        if (path[left+2*dx][right+2*dy] == []):
                            q.append((left+(2*dx), right+(2*dy)))
                            path[left+2*dx][right+2*dy] = path[left][right] + [(left + 2*dx,right + 2*dy)]
                            if ([left+2*dx,right+2*dy] not in W_CAMP):
                                return ['J', path[left+2*dx][right+2*dy]]
                    #condition 1b    
                    elif (condition == "condition1b"):
                        if (path[left+2*dx][right+2*dy] == []):
                                q.append((left+(2*dx), right+(2*dy)))
                                path[left+2*dx][right+2*dy] = path[left][right] + [(left + 2*dx,right + 2*dy)]
                                if (((left+(2*dx)) <= i) and ((right + (2*dy)) <= j)):
                                    return ['J', path[left+2*dx][right+2*dy]]
                    #condition 3
                    elif (condition == "condition3"):
                        if (path[left+2*dx][right+2*dy] == []):
                            q.append((left+(2*dx), right+(2*dy)))
                            path[left+2*dx][right+2*dy] = path[left][right] + [(left + 2*dx,right + 2*dy)]
                            if ([left+2*dx,right+2*dy] in B_CAMP):      #CHANGE : not in W_CAMP to in B_CAMP
                                return ['J', path[left+2*dx][right+2*dy]]
                        
def single_E_move_B(search_space, surround, condition):
    for i,j in search_space:                                                          #for each of the 19 pieces
                for dx, dy, name in surround:                                         #each surrounding
                    if (0<= i + dx <=15 and 0 <= j + dy <= 15):                         #check if inside matrix
                        #condition 1 - when pieces inside camp
                        #1a) inside to outside camp 
                        if (condition == "condition1a"):
                            if (board[i + dx][j + dy] == '.' and ([i + dx,j + dy] not in B_CAMP)): 
                                walking_path = [(i,j),(i+dx,j+dy)]
                                return ['E', walking_path]
                        #1b) within camp
                        if (condition == "condition1b"):
                            if (board[i + dx][j + dy] == '.' and ((i+dx > i) or (j + dy > j))): 
                                walking_path = [(i,j),(i+dx,j+dy)]
                                return ['E', walking_path]
                        #condition 2 = not in any camp
                        if (condition == "condition2"):
                            if (board[i + dx][j + dy] == '.' and ([i + dx,j + dy] not in B_CAMP)): 
                                walking_path = [(i,j),(i+dx,j+dy)]
                                return ['E', walking_path]
                        #condition 3 - inside opponent's camp
                        if (condition == "condition3"):
                            if (board[i + dx][j + dy] == '.' and ([i + dx,j + dy] in W_CAMP)): 
                                walking_path = [(i,j),(i+dx,j+dy)]
                                return ['E', walking_path]
                            
def single_J_move_B(search_space, surround, condition):
    for i,j in search_space:
        path = [[[] for _ in range(16)] for _ in range(16)]
        q = []
        q.append((i,j))
        path[i][j] += [(i,j)]

        while (len(q) > 0):         #running condition - frontier cannot be empty
            left, right = q.pop(0)
            #children/possible further jumps
            for dx, dy, name in surround:
                if ((0<= left + dx <=15) and (0 <= right + dy <= 15) and (0<= left + 2*dx <=15) and (0 <= right + 2*dy <= 15) and (board[left + dx][right + dy] != '.') and (board[left + 2*dx][right + 2*dy] == '.')):
                    #condition 1a or condition 2
                    if (condition == "condition1a" or condition == "condition2" ):
                        if (path[left+2*dx][right+2*dy] == []):
                            q.append((left+(2*dx), right+(2*dy)))
                            path[left+2*dx][right+2*dy] = path[left][right] + [(left + 2*dx,right + 2*dy)]
                            if ([left+2*dx,right+2*dy] not in B_CAMP):
                                return ['J', path[left+2*dx][right+2*dy]]
                    #condition 1b    
                    elif (condition == "condition1b"):
                        if (path[left+2*dx][right+2*dy] == []):
                                q.append((left+(2*dx), right+(2*dy)))
                                path[left+2*dx][right+2*dy] = path[left][right] + [(left + 2*dx,right + 2*dy)]
                                if (((left+(2*dx)) >= i) and ((right + (2*dy)) >= j)):
                                    return ['J', path[left+2*dx][right+2*dy]]
                    #condition 3
                    elif (condition == "condition3"):
                        if (path[left+2*dx][right+2*dy] == []):
                            q.append((left+(2*dx), right+(2*dy)))
                            path[left+2*dx][right+2*dy] = path[left][right] + [(left + 2*dx,right + 2*dy)]
                            if ([left+2*dx,right+2*dy] in W_CAMP):      #CHANGE : not in W_CAMP to in B_CAMP
                                return ['J', path[left+2*dx][right+2*dy]]
                        

def single_play(board, player_name, remaining_time):
    ######MY_PLAYER = WHITE
    if (player_name == 'W'):                                #FOR EACH PIECE W
        #_________________________________________________________________________________________________________________________________
        #CONDITION 1: if at least one piece inside own camp
        # 1a) inside to outside camp (PUSHING OUT W FROM W's CAMP WHEN AT LEAST 1 W in W_CAMP)
        # 1b) within camp, if 1a is not possible (WHEN W in W_CAMP cannot move out, then move W inside W_CAMP further away from corner)
        #_________________________________________________________________________________________________________________________________
        if (no_W_in_W >0):
            
            ##Condition 1a)
            #E move
            result = single_E_move_W(W_in_W, surround_W, "condition1a")
            if (result):    return result
            
            #J moves
            result = single_J_move_W(W_in_W, surround_W, "condition1a")
            if (result):    return result
            
            ##Condition 1b)
            #E move
            result = single_E_move_W(W_in_W, surround_W_awayfrom_camp, "condition1b")
            if (result):    return result
            
            #J move
            result = single_J_move_W(W_in_W, surround_W, "condition1b")
            if (result):    return result
                
        #__________________________________________________________________________________________________________________________________________________________________
        #CONDITION 2 and 3:
            #2: player cannot make a move that starts outside my camp and ends up inside my camp
            #3: once a piece has reached the opposing camp, a play cannot result in that piece leaving the camp (search space is only the W pieces in B_CAMP)
        #__________________________________________________________________________________________________________________________________________________________________


        #FOR CONDITION 2, search space is all W pieces not in either of the camps
        W_outside_camps = []
        for v in W_pos: W_outside_camps.append(v)
        for val in W_pos:
            if (val in W_in_B): W_outside_camps.remove(val)
        
        #Condition 2
        #E move
        if (len(W_outside_camps)>0):
            result = single_E_move_W(W_outside_camps, surround_W, "condition2")
            if (result):    return result

        #Condition 3
        #E move
        if (len(W_in_B) > 0):
            result = single_E_move_W(W_in_B, surround_W, "condition3")
            if (result):    return result

        #Condition 2
        #J move
        if (len(W_outside_camps)>0):
            result = single_J_move_W(W_outside_camps, surround_W, "condition2")
            if (result):    return result
            
        #Condition 3
        #J move
        if (len(W_in_B) > 0):
            result = single_J_move_W(W_in_B, surround_W, "condition3")
            if (result):    return result

    ######MY_PLAYER = BLACK
    if (player_name == 'B'):                                #FOR EACH PIECE W
        #_________________________________________________________________________________________________________________________________
        #CONDITION 1: if at least one piece inside own camp
        # 1a) inside to outside camp (PUSHING OUT W FROM W's CAMP WHEN AT LEAST 1 W in W_CAMP)
        # 1b) within camp, if 1a is not possible (WHEN W in W_CAMP cannot move out, then move W inside W_CAMP further away from corner)
        #_________________________________________________________________________________________________________________________________
        if (no_B_in_B >0):
            
            ##Condition 1a)
            #E move
            result = single_E_move_B(B_in_B, surround_B, "condition1a")
            if (result):    return result
            
            #J moves
            result = single_J_move_B(B_in_B, surround_B, "condition1a")
            if (result):    return result
            
            ##Condition 1b)
            #E move
            result = single_E_move_B(B_in_B, surround_B_awayfrom_camp, "condition1b")
            if (result):    return result
            
            #J move
            result = single_J_move_B(B_in_B, surround_B, "condition1b")
            if (result):    return result
                
        #__________________________________________________________________________________________________________________________________________________________________
        #CONDITION 2 and 3:
            #2: player cannot make a move that starts outside my camp and ends up inside my camp
            #3: once a piece has reached the opposing camp, a play cannot result in that piece leaving the camp (search space is only the W pieces in B_CAMP)
        #__________________________________________________________________________________________________________________________________________________________________


        #FOR CONDITION 2, search space is all W pieces not in either of the camps
        B_outside_camps = []
        for v in B_pos: B_outside_camps.append(v)
        for val in B_pos:
            if (val in B_in_W): B_outside_camps.remove(val)
        
        #Condition 2
        #E move
        if (len(B_outside_camps)>0):
            result = single_E_move_B(B_outside_camps, surround_B, "condition2")
            if (result):    return result

        #Condition 3
        #E move
        if (len(B_in_W) > 0):
            result = single_E_move_B(B_in_W, surround_B, "condition3")
            if (result):    return result

        #Condition 2
        #J move
        if (len(B_outside_camps)>0):
            result = single_J_move_B(B_outside_camps, surround_B, "condition2")
            if (result):    return result
            
        #Condition 3
        #J move
        if (len(B_in_W) > 0):
            result = single_J_move_B(B_in_W, surround_B, "condition3")
            if (result):    return result    

################################ MAIN ################################

if __name__ == "__main__":
    
    #READING DATA FROM INPUT.TXT
    f = open("input.txt")
    inp = f.read().split('\n')
    f.close()
    game_type = inp[0].strip()  							6#game type
    player_name = inp[1].strip()
    if (player_name == "WHITE"):    						#player type 
        player_name = 'W'
        opponent_name = 'B'
    else:
        player_name = 'B'
        opponent_name ='W' 
    remaining_time = inp[2].strip()    						#remaining time
    board = []                      						#read board state
    board_index = 3
    for i in range (16):
        line = inp[board_index].strip()
        board_line = []
        for j in range (16):    board_line.append(line[j])  #added to the board
        board.append(board_line)
        board_index += 1    
            
    
    #ENTERING TURN
    if (game_type == "SINGLE"):
        #DIAGONALTRAVERSE AND STORING Bs and Ws
        N = len(board)
        for k in range (0, N):
            i = k; j = 0
            while (i >= 0):
                if (board[i][j] == 'W'):    W_pos.append([i,j])
                if (board[i][j] == 'B'):    B_pos.append([i,j])
                if ([i,j] in B_CAMP and board[i][j] == 'B'): no_B_in_B += 1; B_in_B.append([i,j])
                if ([i,j] in W_CAMP and board[i][j] == 'B'): no_B_in_W += 1; B_in_W.append([i,j])
                if ([i,j] in B_CAMP and board[i][j] == 'W'): no_W_in_B += 1; W_in_B.append([i,j])
                if ([i,j] in W_CAMP and board[i][j] == 'W'): no_W_in_W += 1; W_in_W.append([i,j])
                i -= 1; j += 1
        for k in range (1, N):
            i = N-1; j = k
            while (j <= N-1):
                if (board[i][j] == 'W'):    W_pos.append([i,j])
                if (board[i][j] == 'B'):    B_pos.append([i,j])
                if ([i,j] in B_CAMP and board[i][j] == 'B'): no_B_in_B += 1; B_in_B.append([i,j])
                if ([i,j] in W_CAMP and board[i][j] == 'B'): no_B_in_W += 1; B_in_W.append([i,j])
                if ([i,j] in B_CAMP and board[i][j] == 'W'): no_W_in_B += 1; W_in_B.append([i,j])
                if ([i,j] in W_CAMP and board[i][j] == 'W'): no_W_in_W += 1; W_in_W.append([i,j])
                i -= 1; j += 1
        B_pos.reverse()
        B_in_B.reverse()
        B_in_W.reverse()
        
        move = []
        move = single_play(board, player_name, remaining_time)  
        f = open("output.txt","w")
        printResult(move[0], move[1])
        f.close()
        
    else:
        N = len(board)
        for k in range (0, N):
            i = k; j = 0
            while (i >= 0):
                if (board[i][j] == 'W'):    W_pos.append([i,j])
                if (board[i][j] == 'B'):    B_pos.append([i,j])
                if ([i,j] in B_CAMP and board[i][j] == 'B'): no_B_in_B += 1; B_in_B.append([i,j])
                if ([i,j] in W_CAMP and board[i][j] == 'B'): no_B_in_W += 1; B_in_W.append([i,j])
                if ([i,j] in B_CAMP and board[i][j] == 'W'): no_W_in_B += 1; W_in_B.append([i,j])
                if ([i,j] in W_CAMP and board[i][j] == 'W'): no_W_in_W += 1; W_in_W.append([i,j])
                i -= 1; j += 1
        for k in range (1, N):
            i = N-1; j = k
            while (j <= N-1):
                if (board[i][j] == 'W'):    W_pos.append([i,j])
                if (board[i][j] == 'B'):    B_pos.append([i,j])
                if ([i,j] in B_CAMP and board[i][j] == 'B'): no_B_in_B += 1; B_in_B.append([i,j])
                if ([i,j] in W_CAMP and board[i][j] == 'B'): no_B_in_W += 1; B_in_W.append([i,j])
                if ([i,j] in B_CAMP and board[i][j] == 'W'): no_W_in_B += 1; W_in_B.append([i,j])
                if ([i,j] in W_CAMP and board[i][j] == 'W'): no_W_in_W += 1; W_in_W.append([i,j])
                i -= 1; j += 1
        B_pos.reverse()
        B_in_B.reverse()
        B_in_W.reverse()

            
        depth = 2
        if (float(remaining_time) < 180):
            depth = 3
        if (float(remaining_time) < 100):
            depth = 2
        if (float(remaining_time) < 20):
            depth = 1
        depth = 2; t = 1.5
        eta = float(remaining_time)
        if (eta < 180):
            depth = 3;
        if (eta < 100):
            depth = 2
        if (eta < 20):
            depth = 1
        #If almost winning, player = white
        if (player_name == "W" and no_W_in_B >= 14):
            if (eta >180):      depth = 3; t = 4
            if (eta > 100):   depth = 3; t = 2
            if (eta > 50):    depth = 2; t = 1.5
        #If almost winning, player = black
        if ("player_name == \"B\" and ",no_B_in_W," >= 14"):
            if (eta >180):      depth = 3; t = 4
            if (eta > 100):   depth = 3; t = 2
            if (eta > 50):    depth = 2; t = 1.5
        move = []
        move = game(board, player_name, remaining_time, t)
        #If no output found at depth, then: 
        if (move[0] == None and eta > 20):                           
            move = []; depth = 1; t = 1.6
            move = game(board, player_name, remaining_time, t)
        #If no output found at depth 1, then: 
        if (move[0] == None):                                                     
            move = [];
            move = single_play(board, player_name, remaining_time)
        
        f = open("output.txt","w")
        printResult(move[0], move[1])
        f.close()
