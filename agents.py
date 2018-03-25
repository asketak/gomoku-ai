#!/usr/bin/env python

#Fall 2013 COLUMBIA UNIVERSITY
#COMS W4701 Artificial Intelligence
#Assignment 3: Gomoku
#
#UNI: hs2762
#Name: Hao-Hsin Shih

import sys
import os
import os.path
import re
import time
import string
import copy
import random

########################################################################
########################################################################
# INITIATE THE GAME
#use infinity as a big number in Search
infinity = 999999999
size_move_list = 15
DEPTH_TO_STOP = 5

time_limit = int(sys.argv[3]); #10#unit: second
winning_chain_length = int(sys.argv[2]) #5
board_dimension = int(sys.argv[1]) #15#should be much bigger than winning_chain_length

#black stone: x; white stone: o;empty space:
#initial score
score = 0
#build initial board
board = [['.' for m in range(board_dimension)] for n in range(board_dimension) ]
#left to right, up to down, up_left to down_right, down_left to up right
board2 = [ [ [ ['z','z','z','z'] for m in range(board_dimension)] for n in range(board_dimension)], [ [ ['z','z','z','z'] for m in range(board_dimension)] for n in range(board_dimension)]  ]
#info of black: board[1]
#info of white: board[0]

#black stone: turn = 1; white stone: turn = 0. black stat fisrt
turn = 1
#variable to get coordinate input for user or agent [y, x]
coordinate = [0,0]
#search window
plus = [
        [[-1,-1], [-1,0], [-1,1]],
        [[0,-1],  [0,0],  [0,1]],
        [[1,-1],  [1,0],  [1,1]],
       ]
#step_history records the movement history
#each element is in format [y, x, whose turn(order 0 or 1) ]
step_history = []
#move_List: the best move ordered by score

#each element is in format [y, x, score]
#attacking list
#defending_list
move_list = [[],[]]

########################################################################
########################################################################
# SUB FUNCTIONS
def show_game(board,size):
    print '\\',
    for t in range(size):
        if t >= 10:
            print t -10,
        else:
            print t,

    print ''
    for i in range(size):
        if i >= 10:
            print i-10,
        else:
            print i,
        for j in range(size):
            print '%s' %(board[i][j]),
        print ''

def get_coordinate( size ,board):
    while True:
        output_list = []
        print 'please enter the coordinate in format x y'
        get = raw_input()

        # # return other command
        # if get == 'undo':
        #     return ['undo']
        # if get == 'surrender':
        #     return ['surrender']

        input_list = get.strip(' ').split(' ')
        #examine if x y is number
        if len(input_list) != 2:
            print 'ERROR INFO: invalid input, please try again'
            continue
        for s in input_list:
            if s.isdigit():
                if int(s) < size and int(s) >=0:
                    output_list.append(int(s))
            else:
                print 'ERROR INFO: invalid input, please try again'
        if len(output_list) != 2:
            print 'ERROR INFO: invalid input, please try again'
            continue

        if board[output_list[0]][output_list[1]] != '.':
            print 'A stone is already at this position, please try again'
            continue
        else:
            return output_list
########################################################################
########################################################################
#EVALUATION
def evaluation(board2, turn, board_dimension):

    value = 0

    if turn%2 == 1:
        positive = board2[1]
        negative = board2[0]
    else:
        positive = board2[0]
        negative = board2[1]

    for i in range(board_dimension):
        for j in range(board_dimension):
            value += score_table[projection(positive[i][j])] - score_table[projection(negative[i][j])]

    return value


########################################################################
########################################################################
#SEARCH
def abMax(depth, a, b, time_anchor, time_limit, move_list, step_history, turn, board, board_dimension, winning_chain_length, board2):
    if time.time() - time_anchor >  time_limit or game_over(step_history, turn, board, board_dimension, winning_chain_length) or depth <= 0:
        return evaluation(board2, turn, board_dimension)

    v = -infinity
    #take the first move in move_list and output a new move_list
    for move in move_list[turn%2]:
        #print len(move_list[turn%2])
        new_board = copy.deepcopy(board)

        #print move
        if turn%2 == 1:
            new_board[move[0]][move[1]] = 'x'
        else:
            new_board[move[0]][move[1]] = 'o'

        new_step_history = copy.deepcopy(step_history)
        new_step_history.append([move[1],move[0],turn])

        new_board2 =  copy.deepcopy(board2)
        new_board2[1] = info_update( 1, board_dimension, new_board, new_board2[1], current_move )
        new_board2[0] = info_update( 2, board_dimension, new_board, new_board2[0], current_move )

        new_move_list = copy.deepcopy(move_list)

        for m in range(len(new_move_list[turn%2])):
            point = score_table[projection(new_board2[turn%2][new_move_list[turn%2][m][0]][new_move_list[turn%2][m][1]])]
            if point >= new_move_list[turn%2][m][2]:
                new_move_list[turn%2][m][2] = score_table[projection(new_board2[turn%2][new_move_list[turn%2][m][0]][new_move_list[turn%2][m][1]])]

        for k in range(2):
            for i in range(3):
                for j in range(3):
                    w_x = move[1]+plus[i][j][1]
                    w_y = move[0]+plus[i][j][0]

                    if w_x >= 0 and w_y >= 0 and w_x <= board_dimension-1 and w_y <= board_dimension-1 and new_board[w_y][w_x] == '.':
                        s = score_table[projection(new_board2[k%2][w_y][w_x])]

                    lock = 0
                    for item in new_move_list[k%2]:
                        if item[0] == w_y and item[1] ==  w_x:
                            lock = 1
                        else:
                            lock = 0

                    if w_x >= 0 and w_y >= 0 and w_x <= board_dimension-1 and w_y <= board_dimension-1 and new_board[w_y][w_x] == '.' and [w_y,w_x,s] not in new_move_list[turn%2] and lock != 1:
                        #print [w_y,w_x,s]
                        new_move_list[k%2].append([w_y,w_x,s])
                        new_move_list[k%2] = sorted(new_move_list[k%2], key=lambda x: x[2] , reverse=True)

                        if len(new_move_list[k%2]) > size_move_list:
                           new_move_list[k%2].pop(size_move_list)

        for s in range(2):
            temp_list = []
            for move in new_move_list[s]:
                if new_board[move[0]][move[1]] == '.':
                    temp_list.append(move)
            new_move_list[s] = temp_list[:]
        #randomly switch the move in move_list if they have same evaluation
        for s in range(2):
            count = 0
            temp = []
            rand_score = move_list[s][0][2]

            for item in new_move_list[s]:
                if item[2] == rand_score:
                    count += 1
            if count >= 2:
                new_move_list[s][0:count] = random.sample(new_move_list[s][0:count], count)

        score = abMin(depth-1, a, b, time_anchor, time_limit, new_move_list, new_step_history, turn+1, new_board, board_dimension, winning_chain_length, new_board2)

        v = max(v,score)
        if v >= b:
            return  v
        a = max(a,v)


    return v

def abMin(depth, a, b, time_anchor, time_limit, move_list, step_history, turn, board, board_dimension, winning_chain_length, board2):
    if time.time() - time_anchor >  time_limit or game_over(step_history, turn, board, board_dimension, winning_chain_length) or depth <= 0:
        return 0-evaluation(board2, turn, board_dimension)

    v = infinity
    for move in move_list[turn%2]:
        new_board = copy.deepcopy(board)

        if turn%2 == 1:
            new_board[move[0]][move[1]] = 'x'
        else:
            new_board[move[0]][move[1]] = 'o'

        new_step_history = copy.deepcopy(step_history)
        new_step_history.append([move[1],move[0],turn])

        new_board2 =  copy.deepcopy(board2)
        new_board2[1] = info_update( 1, board_dimension, new_board, new_board2[1], current_move )
        new_board2[0] = info_update( 2, board_dimension, new_board, new_board2[0], current_move )
        new_move_list = copy.deepcopy(move_list)

        for m in range(len(new_move_list[turn%2])):
            point = score_table[projection(new_board2[turn%2][new_move_list[turn%2][m][0]][new_move_list[turn%2][m][1]])]
            if point >= new_move_list[turn%2][m][2]:
                new_move_list[turn%2][m][2] = score_table[projection(new_board2[turn%2][new_move_list[turn%2][m][0]][new_move_list[turn%2][m][1]])]


        for k in range(2):
            for i in range(3):
                for j in range(3):
                    w_x = move[1]+plus[i][j][1]
                    w_y = move[0]+plus[i][j][0]

                    if w_x >= 0 and w_y >= 0 and w_x <= board_dimension-1 and w_y <= board_dimension-1 and new_board[w_y][w_x] == '.':
                        s = score_table[projection(new_board2[k%2][w_y][w_x])]

                    lock = 0
                    for item in new_move_list[k%2]:
                        if item[0] == w_y and item[1] ==  w_x:
                            lock = 1
                        else:
                            lock = 0

                    if w_x >= 0 and w_y >= 0 and w_x <= board_dimension-1 and w_y <= board_dimension-1 and new_board[w_y][w_x] == '.' and [w_y,w_x,s] not in new_move_list[turn%2] and lock != 1:
                        #print [w_y,w_x,s]
                        new_move_list[k%2].append([w_y,w_x,s])
                        new_move_list[k%2] = sorted(new_move_list[k%2], key=lambda x: x[2] , reverse=True)

                        if len(new_move_list[k%2]) > size_move_list:
                           new_move_list[k%2].pop(size_move_list)

        for s in range(2):
            temp_list = []
            for move in new_move_list[s]:
                if new_board[move[0]][move[1]] == '.':
                    temp_list.append(move)
            new_move_list[s] = temp_list[:]
        #randomly switch the move in move_list if they have same evaluation
        for s in range(2):
            count = 0
            temp = []
            rand_score = move_list[s][0][2]

            for item in new_move_list[s]:
                if item[2] == rand_score:
                    count += 1
            if count >= 2:
                new_move_list[s][0:count] = random.sample(new_move_list[s][0:count], count)


        score = abMax(depth-1, a, b, time_anchor, time_limit, new_move_list, new_step_history, turn+1, new_board, board_dimension, winning_chain_length, new_board2)

        v = min(v,score)
        if v <= a:
            return  v
        b = min(b,v)


    return v

########################################################################
########################################################################
# ALPHA-BELTA SERACH
def ab_search (time_limit, move_list, step_history, turn, board, board_dimension, winning_chain_length, board2):
    depth = DEPTH_TO_STOP
    rank = []
    step_time_limit = int(round(time_limit / len(move_list[turn%2])))
    for move in move_list[turn%2]:
        time_anchor = time.time()
        value = abMax(depth, -infinity, infinity, time_anchor, step_time_limit, move_list, step_history, turn, board, board_dimension, winning_chain_length, board2)
        rank.append([value,move])

    rank = sorted(rank, key=lambda x: x[0] , reverse=True)
    #return rank
    return rank[0][1]

########################################################################
########################################################################
# GAME OVER
black_win = ['x' for i in range(winning_chain_length)]
white_win = ['o' for i in range(winning_chain_length)]
def game_over(step_history, turn, board, board_dimension, winning_chain_length):

    if turn != 1: # 1 = fisrt turn
        last_move = step_history[len(step_history)-1]
        y = last_move[0]
        x = last_move[1]

        #to get boundary
        bound_x1 = x - winning_chain_length +1
        if bound_x1 < 0:
            bound_x1 = 0
        bound_y1 = y - winning_chain_length +1
        if bound_y1 < 0:
            bound_y1 = 0
        bound_x2 = x + winning_chain_length-1
        if bound_x2 > board_dimension-1:
            bound_x2 = board_dimension-1
        bound_y2 = y + winning_chain_length-1
        if bound_y2 > board_dimension-1:
            bound_y2 = board_dimension-1

        if turn%2 == 1: #black stone
            target = white_win
        else: #white stone
            target = black_win

        #direction horrizontal
        for i in range(bound_x2 - winning_chain_length + 1 - bound_x1 +1):
            if  bound_x1 + i + winning_chain_length < board_dimension -1:
                if board[y][bound_x1 + i:bound_x1 + i + winning_chain_length] == target:
                    return True
        #direction vertical
        for j in range(bound_y2 - winning_chain_length + 1 - bound_y1 +1):
            temp = []
            for m in range(winning_chain_length):

                if bound_y1+j+m > board_dimension -1 or  bound_y1+j+m < 0:
                    break
                temp.append(board[bound_y1+j+m][x])

            if  temp == target:
                return True

        #direction diagonal up_left to down_right
        d_x1 = x - bound_x1
        d_y1 = y - bound_y1
        if d_x1 > d_y1:
            nb_x1 = x - d_y1
            nb_y1 = bound_y1
        else:
            nb_x1 = bound_x1
            nb_y1 = y - d_x1

        d_x2 = bound_x2 - x
        d_y2 = bound_y2 - y
        if d_x2 > d_y2:
            nb_x2 = x + d_y2
            nb_y2 = bound_y2
        else:
            nb_x2 = bound_x2
            nb_y2 = y + d_x2

        for k in range(nb_x2 - winning_chain_length - nb_x1 +1 +1):
            temp = []
            for m in range(winning_chain_length):
                if nb_y1+k+m > board_dimension - 1 or nb_y1+k+m < 0 or nb_x1+k+m > board_dimension - 1 or nb_x1+k+m < 0:
                    break
                temp.append(board[nb_y1+k+m][nb_x1+k+m])
            if  temp == target:
                return True

        #direction diagonal down_left to up_right
        d_x1 = x - bound_x1
        d_y1 = bound_y2 - y
        if d_x1 > d_y1:
            nb_x1 = x - d_y1
            nb_y1 = bound_y2
        else:
            nb_x1 = bound_x1
            nb_y1 = y + d_x1

        d_x2 = bound_x2 - x
        d_y2 = y - bound_y1
        if d_x2 > d_y2:
            nb_x2 = x + d_y2
            nb_y2 = bound_y1
        else:
            nb_x2 = bound_x2
            nb_y2 = y - d_x2

        for k in range(nb_x2 - winning_chain_length - nb_x1 +1 +1):
            temp = []
            for m in range(winning_chain_length):
                if nb_y1-k-m > board_dimension - 1 or nb_y1-k-m < 0 or nb_x1+k+m > board_dimension - 1 or nb_x1+k+m < 0:
                    break

                temp.append(board[nb_y1-k-m][nb_x1+k+m])
            if  temp == target:
                return True

        return False

    else: #turn = 1:
        return False

########################################################################
########################################################################
# UPDATE BOARD2 INFO
def info_update(turn, board_dimension, board, board_info, move):

    board_temp = board_info
    c_y = move[0]
    c_x = move[1]

    #direction horrizontal
    for i in range(5):
        y = c_y
        x = c_x - 2 + i
        if  y >= 0 and y <= board_dimension-1 and x >= 0 and x <= board_dimension-1 and  board[y][x] == '.':
            board_temp[y][x] =  type_match(y,x,board,turn,board_dimension)
        else:
            pass
    #direction vertical
    for i in range(5):
        y = c_y - 2 + i
        x = c_x
        if  y >= 0 and y <= board_dimension-1 and x >= 0 and x <= board_dimension-1 and  board[y][x] == '.':
            board_temp[y][x] =  type_match(y,x,board,turn,board_dimension)
        else:
            pass
    #direction diagonal up_left to down_right
    for i in range(5):
        y = c_y - 2 + i
        x = c_x - 2 + i
        if  y >= 0 and y <= board_dimension-1 and x >= 0 and x <= board_dimension-1 and  board[y][x] == '.':
            board_temp[y][x] =  type_match(y,x,board,turn,board_dimension)
        else:
            pass
    #direction diagonal down_left to up_right
    for i in range(5):
        y = c_y + 2 - i
        x = c_x - 2 + i

        if  y >= 0 and y <= board_dimension-1 and x >= 0 and x <= board_dimension-1 and  board[y][x] == '.':
            board_temp[y][x] =  type_match(y,x,board,turn,board_dimension)
        else:
            pass

    return board_temp
########################################################################
########################################################################
# UPDATE ONE POSITION INFO
def type_match(y,x,board,turn,board_dimension):

    new = []

    window = []
    for w in range(5):
        string = ''
        #direction horrizontal
        for i in range(5):
            temp_y = y
            temp_x = x - 4 + w + i
            if temp_y < 0 or temp_y > board_dimension-1 or temp_x < 0 or temp_x > board_dimension-1:
                string = string + 'e'
            else:
                if turn%2 == 1: #black
                    if board[temp_y][temp_x] == 'x':
                        string = string + '1'
                    else:
                        if board[temp_y][temp_x] == 'o':
                            string = string + '2'
                        else:
                            string = string + '0'
                else: #white
                    if board[temp_y][temp_x] == 'o':
                        string = string + '1'
                    else:
                        if board[temp_y][temp_x] == 'x':
                            string = string + '2'
                        else:
                            string = string + '0'

        if type_table.has_key(string):
            window.append( [type_table[string],score_table[(type_table[string])]])
        else:
            window.append(['z', 0 ])

    window = sorted(window, key=lambda x: x[1] , reverse=True)
    new.append(window[0][0])

    window = []
    for w in range(5):
        string = ''
        #direction vertical
        for i in range(5):
            temp_y = y - 4 + w + i
            temp_x = x
            if temp_y < 0 or temp_y > board_dimension-1 or temp_x < 0 or temp_x > board_dimension-1:
                string = string + 'e'
            else:
                if turn%2 == 1: #black
                    #print temp_y
                    if board[temp_y][temp_x] == 'x':
                        string = string + '1'
                    else:
                        if board[temp_y][temp_x] == 'o':
                            string = string + '2'
                        else:
                            string = string + '0'
                else: #white
                    if board[temp_y][temp_x] == 'o':
                        string = string + '1'
                    else:
                        if board[temp_y][temp_x] == 'x':
                            string = string + '2'
                        else:
                            string = string + '0'

        if type_table.has_key(string):
            window.append( [type_table[string],score_table[(type_table[string])]])
        else:
            window.append(['z', 0 ])

    window = sorted(window, key=lambda x: x[1] , reverse=True)
    new.append(window[0][0])

    window = []
    for w in range(5):
        string = ''
        #direction diagonal up_left to down_right
        for i in range(5):
            temp_y = y - 4 + w + i
            temp_x = x - 4 + w + i
            if temp_y < 0 or temp_y > board_dimension-1 or temp_x < 0 or temp_x > board_dimension-1:
                string = string + 'e'
            else:
                if turn%2 == 1: #black
                    if board[temp_y][temp_x] == 'x':
                        string = string + '1'
                    else:
                        if board[temp_y][temp_x] == 'o':
                            string = string + '2'
                        else:
                            string = string + '0'
                else: #white
                    if board[temp_y][temp_x] == 'o':
                        string = string + '1'
                    else:
                        if board[temp_y][temp_x] == 'x':
                            string = string + '2'
                        else:
                            string = string + '0'

        if type_table.has_key(string):
            window.append( [type_table[string],score_table[(type_table[string])]])
        else:
            window.append(['z', 0 ])

    window = sorted(window, key=lambda x: x[1] , reverse=True)
    new.append(window[0][0])

    window = []
    for w in range(5):
        string = ''
        #direction diagonal down_left to up_right
        for i in range(5):
            temp_y = y + 4 - w - i
            temp_x = x - 4 + w + i
            if temp_y < 0 or temp_y > board_dimension-1 or temp_x < 0 or temp_x > board_dimension-1:
                string = string + 'e'
            else:
                if turn%2 == 1: #black
                    if board[temp_y][temp_x] == 'x':
                        string = string + '1'
                    else:
                        if board[temp_y][temp_x] == 'o':
                            string = string + '2'
                        else:
                            string = string + '0'
                else: #white
                    if board[temp_y][temp_x] == 'o':
                        string = string + '1'
                    else:
                        if board[temp_y][temp_x] == 'x':
                            string = string + '2'
                        else:
                            string = string + '0'

                #print string
        if type_table.has_key(string):
            window.append( [type_table[string],score_table[(type_table[string])]])
        else:
            window.append(['z', 0 ])

    window = sorted(window, key=lambda x: x[1] , reverse=True)
    new.append(window[0][0])
    # if y == 4 and x == 10:
    #     print 'window',window
    #     print 'new',new

    return new

#search_region = [[ 0 for m in range(board_dimension)] for n in range(board_dimension) ]
#hash for searching local board state
type_table = {  '00000': 'z',
                '00002': 'z',
                '00020': 'z',
                '00022': 'l_1',
                '00200': 'z',
                '00202': 'l_1',
                '00220': 'b_2',
                '00222': 'b_3',
                '02000': 'z',
                '02002': 'l_1',
                '02020': 'l_1',
                '02022': 'b_3',
                '02200': 'b_2',
                '02202': 'b_3',
                '02220': 'b_3',
                '02222': 'b_4',
                '22000': 'l_1',
                '20002': 'z',
                '20020': 'z',
                '20022': 'b_3',
                '20200': 'l_1',
                '20202': 'b_3',
                '20220': 'b_3',
                '20222': 'b_4',
                '22000': 'l_1',
                '22002': 'b_3',
                '22020': 'b_3',
                '22022': 'b_4',
                '22200': 'l_2',
                '22202': 'b_4',
                '22220': 'b_4',
                '00001': 'l_1', ##############################################################
                '00021': 'z',
                '00201': 'z',
                '00221': 'l_1',
                '02001': 'z',
                '02021': 'l_1',
                '02201': 'b_2',
                '02221': 'l_2',
                '20001': 'l_1',
                '20021': 'b_2',
                '20201': 'b_2',
                '20221': 'b_3',
                '22001': 'l_1',
                '22021': 'b_3',
                '22201': 'l_2',
                '00210': 'z',
                '02010': 'z',
                '02210': 'z',
                '20010': 'l_1',
                '20210': 'l_1',
                '22010': 'l_1',
                '22210': 'z',
                '00010': 'l_1',
                '00011': 'b_2',
                '00211': 'z',
                '20011': 'b_2',
                '02011': 'b_2',
                '22011': 'l_2',
                '20211': 'b_2',
                '02211': 'b_2',
                '00101': 'l_2',
                '20101': 'l_2',
                '02101': 'b_2',
                '22101': 'b_2',
                '00110': 'l_2',
                '00112': 'b_2',
                '20110': 'b_2',
                '02110': 'b_2',
                '22110': 'l_1',
                '00111': 'b_3',
                '20111': 'b_3',
                '02111': 'z',
                '01000': 'l_1',
                '01001': 'l_2',
                '21001': 'b_2',
                '01010': 'l_2',
                '21010': 'b_2',
                '01011': 'l_3',
                '21011': 'b_3',
                '01101': 'l_3',
                '01120': 'z',
                '21101': 'b_3',
                '01110': 'l_3',
                '21110': 'b_3',
                '01112': 'b_3',
                '01111': 'l_4',
                '10022': 'z',
                '10220': 'z',
                '10000': 'z',
                '10010': 'l_2',
                '10012': 'b_2',
                '10011': 'l_3',
                '10100': 'l_2',
                '10102': 'b_2',
                '10120': 'b_2',
                '10122': 'b_2',
                '10101': 'l_3',
                '10110': 'l_3',
                '10112': 'b_3',
                '10111': 'l_4',
                '11000': 'l_2',
                '11020': 'l_2',
                '11002': 'l_2',
                '11022': 'l_2',
                '11200': 'z',
                '11220': 'b_2',
                '11202': 'b_2',
                '11222': 'b_2',
                '11001': 'l_3',
                '11010': 'l_3',
                '11012': 'b_3',
                '11011': 'l_4',
                '11100': 'b_3',
                '11120': 'z',
                '11102': 'b_3',
                '11101': 'l_4',
                '11110': 'l_4',
                '11112': 'b_4'
             }

score_table = { 'l_5' : 100000,
                'l_4' : 10000,
                'db_4' : 10000,
                'b4_l3' :10000,
                'dl_3' : 5000,
                'b3_l3': 1000,
                'b_4' : 500,
                'l_3' : 200,
                'db_3': 100,
                'b_3' : 50,
                'dl_2' : 10,
                'l_2' : 5,
                'b_2' : 3,
                'l_1' : 1,
                'z' : 0
             }
#Projection of type_table to score_table
def projection(type_list):

    if type_list.count('l_5') >= 1:
        return 'l_5'
    elif type_list.count('l_4') >= 1:
        return 'l_4'
    elif type_list.count('b_4') >=2:
        return 'db_4'
    elif type_list.count('b_4') >= 1 and type_list.count('l_3') >= 1:
        return 'b4_l3'
    elif type_list.count('l_3') >= 2:
        return 'dl_3'
    elif type_list.count('b_3') >= 1 and type_list.count('l_3') >= 1:
        return 'b3_l3'
    elif type_list.count('b_4') >= 1:
        return 'b_4'
    elif type_list.count('l_3') >= 1:
        return 'l_3'
    elif type_list.count('b_3') >= 2:
        return 'db_3'
    elif type_list.count('b_3') >= 1:
        return 'b_3'
    elif type_list.count('l_2') >= 2:
        return 'dl_2'
    elif type_list.count('l_2') >= 1:
        return 'l_2'
    elif type_list.count('b_2') >= 1:
        return 'b_2'
    elif type_list.count('l_1') >= 1:
        return 'l_1'
    else:
        return 'z'


########################################################################
########################################################################
#GAME START
while True:
    print 'NEW GAME'
    print 'please select the mode by entering number (1-3):'
    print '1: Battle.'
    print '2: Agent Against Agent(randomly move).'
    print '3: Agent Fight Itself.'
    print '4  Exit.'
    mode = raw_input()
    if len(mode) == 0 or (mode != '1' and mode != '2' and mode != '3' and mode != '4'):
        print 'ERROR INFO: invalid input'
        continue
    if mode == '4':
        print 'EXITED'
        break

    #initial
    turn = 1
    board = [['.' for m in range(board_dimension)] for n in range(board_dimension) ]
    board2 = [ [ [ ['z','z','z','z'] for m in range(board_dimension)] for n in range(board_dimension)], [ [ ['z','z','z','z'] for m in range(board_dimension)] for n in range(board_dimension)]  ]
    score = 0
    step_history = []
    move_list = [[],[]]
    coordinate = [0,0]
    #search_region = [[ 0 for m in range(board_dimension)] for n in range(board_dimension) ]

    black_win = ['x' for i in range(winning_chain_length)]
    white_win = ['o' for i in range(winning_chain_length)]

#####################################################################################
#####################################################################################
#MODE 1
    if mode == '1':
        print 'Which one takes black stone? (1-3)'
        print '1 This Agent.'
        print '2 The Other.'
        print '3 Cancel.'
        order = raw_input()

        if len(order) == 0 or (order != '1' and order != '2' and order != '3'):
            print 'ERROR INFO: invalid input'
            continue

        if order == '1':
            order_num = 1
            print 'this agent takes black stone\n'
        elif order == '2':
            order_num = 0
            print 'this agent takes white stone\n'
        else: #mode == '3':
            print 'CANCELED'
            continue

        #start with follow-moon path
        if order_num == 1:
            yan = int((round(board_dimension-1)/2))
            move_list = [[],[[yan,yan,1000000], [yan-1,yan+1,80000],[yan+1,yan+1,7000]]]

        while True:
            #show the board on the screen
            show_game(board, board_dimension)

            if game_over(step_history, turn, board, board_dimension, winning_chain_length):
                if turn%2 == 1:
                    print 'white stone win!!'
                    break
                else:
                    print 'black stone win!!'
                    break
            if len(step_history)!= 0:
                print 'last move: %d  %d' %(step_history[len(step_history)-1][0] ,step_history[len(step_history)-1][1])
            print 'turn: %d' %(turn)
            if turn%2 == 1:
                print 'black stone\'s turn'
            else:
                print 'white stone\'s turn'


 ################################################################################################
            if turn%2 == order_num:
                #get coordinate from player
                #start with follow-moon path
                #################################################################################
                #black agent
                if order_num == 1: #take black stone

                    # start with fixed position with good probability to win
                    if turn <= 5:
                        if turn == 5:
                            if board[yan][yan] == 'x' and board[yan-1][yan+1] == 'x':
                                #follow-moon mode
                                if board[yan-1][yan] == 'o' and board[yan][yan+1] == 'o':
                                    current_move = [yan-2, yan+2, 7000]
                                elif board[yan-1][yan] == 'o' and board[yan+1][yan+1] == 'o':
                                    current_move = [yan+1, yan-1, 7000]
                                elif board[yan-1][yan] == 'o' and board[yan+1][yan-1] == 'o':
                                    current_move = [yan-2, yan+1, 7000]
                                else:
                                    current_move = [yan-2, yan+2, 7000]
                                    if board[current_move[0]][current_move[1]] != '.':
                                        current_move = [yan+1, yan-1, 7000]
                                        if board[current_move[0]][current_move[1]] != '.':
                                            current_move = [yan-2, yan+1, 7000]
                                #remove path have been visited
                                temp_item = []
                                for item in move_list[turn%2]:
                                    if item[0] == current_move[0] and item[1] == current_move[1]:
                                        temp_item = item
                                        break
                                if len(temp_item) != 0:
                                    move_list[turn%2].remove(temp_item)

                            else:
                                #glass-moon mode
                                if board[yan-1][yan+1] == 'o' and board[yan-1][yan-1] == 'o':
                                    current_move = [yan, yan+2, 7000]
                                elif board[yan-1][yan+1] == 'o' and board[yan+1][yan] == 'o':
                                    current_move = [yan-1, yan-1, 7000]
                                elif board[yan-1][yan+1] == 'o' and board[yan+2][yan] == 'o':
                                    current_move = [yan-1, yan-1, 7000]
                                else:
                                    current_move = [yan, yan+2, 7000]
                                    if board[current_move[0]][current_move[1]] != '.':
                                        current_move = [yan-1, yan-1, 7000]
                                        if board[current_move[0]][current_move[1]] != '.':
                                          current_move = [yan, yan-1, 7000]
                                #remove path have been visited
                                temp_item = []
                                for item in move_list[turn%2]:
                                    if item[0] == current_move[0] and item[1] == current_move[1]:
                                        temp_item = item
                                        break
                                if len(temp_item) != 0:
                                    move_list[turn%2].remove(temp_item)

                            if [yan+1,yan+1,7000] in move_list[turn%2]:
                                move_list[turn%2].remove([yan+1,yan+1,7000])

                        else:
                            current_move = move_list[turn%2][0]
                            move_list[turn%2].remove(current_move)
                            if board[current_move[0]][current_move[1]] != '.':
                                current_move = move_list[turn%2][0]
                                move_list[turn%2].remove(current_move)
                        #print infomation
                        # print move_list[turn%2]
                        # print current_move
                        # print board2[turn%2][current_move[0]][current_move[1]]

                        if current_move in move_list[turn%2]:
                            move_list[turn%2].remove(current_move)


                    else:
                        current_move = ab_search(time_limit, move_list, step_history, turn, board, board_dimension, winning_chain_length, board2)

                        #print information
                        # print move_list[turn%2]
                        # print current_move
                        # print board2[turn%2][current_move[0]][current_move[1]]

                        if current_move in move_list[turn%2]:
                            move_list[turn%2].remove(current_move)

                    coordinate[0] = current_move[0]
                    coordinate[1] = current_move[1]

                # coordinate = get_coordinate( board_dimension ,board)
                # current_move = coordinate
                ####################################################################################
                #white agent
                else: #agent take white

                    current_move = ab_search(time_limit, move_list, step_history, turn, board, board_dimension, winning_chain_length, board2)

                    print move_list[turn%2]
                    print current_move
                    print board2[turn%2][current_move[0]][current_move[1]]

                    if current_move in move_list[turn%2]:
                        move_list[turn%2].remove(current_move)

                    coordinate[0] = current_move[0]
                    coordinate[1] = current_move[1]


                if order_num ==1 : #take black stone
                    board[coordinate[0]][coordinate[1]] = 'x'
                else:
                    board[coordinate[0]][coordinate[1]] = 'o'

                #update info table
                board2[1] = info_update( 1, board_dimension, board, board2[1], current_move )
                board2[0] = info_update( 2, board_dimension, board, board2[0], current_move )
                #update move_list


                for d in range(2):
                    for move in range(len(move_list[d%2])):
                        point = score_table[projection(board2[d%2][move_list[d%2][move][0]][move_list[d%2][move][1]])]
                        if point >= move_list[d%2][move][2]:
                            move_list[d%2][move][2] = score_table[projection(board2[d%2][move_list[d%2][move][0]][move_list[d%2][move][1]])]

                for k in range(2):
                    for i in range(3):
                        for j in range(3):
                            w_x = current_move[1]+plus[i][j][1]
                            w_y = current_move[0]+plus[i][j][0]

                            if w_x >= 0 and w_y >= 0 and w_x <= board_dimension-1 and w_y <= board_dimension-1 and board[w_y][w_x] == '.':
                                s = score_table[projection(board2[k%2][w_y][w_x])]

                            lock = 0
                            for item in move_list[k%2]:
                                if item[0] == w_y and item[1] ==  w_x:
                                    lock = 1
                                else:
                                    lock = 0

                            if w_x >= 0 and w_y >= 0 and w_x <= board_dimension-1 and w_y <= board_dimension-1 and board[w_y][w_x] == '.' and [w_y,w_x,s] not in move_list[turn%2] and lock != 1:
                                #print [w_y,w_x,s]
                                move_list[k%2].append([w_y,w_x,s])
                                move_list[k%2] = sorted(move_list[k%2], key=lambda x: x[2] , reverse=True)

                                if len(move_list[k%2]) > size_move_list:
                                   move_list[k%2].pop(size_move_list)


                for s in range(2):
                    temp_list = []
                    for move in move_list[s]:
                        if board[move[0]][move[1]] == '.':
                            temp_list.append(move)
                    move_list[s] = temp_list[:]
                #randomly switch the move in move_list if they have same evaluation
                for s in range(2):
                    count = 0
                    temp = []
                    rand_score = move_list[s][0][2]

                    for item in move_list[s]:
                        if item[2] == rand_score:
                            count += 1
                    if count >= 2:
                        move_list[s][0:count] = random.sample(move_list[s][0:count], count)

            else:
                #put white player


                #get coordinate from player
                coordinate = get_coordinate( board_dimension ,board)
                current_move = coordinate
                #update the board

                if order_num ==1 : #take black stone
                    board[coordinate[0]][coordinate[1]] = 'o'
                else:
                    board[coordinate[0]][coordinate[1]] = 'x'

                #pritn information
                # print move_list[turn%2]
                # print current_move
                # print board2[turn%2][current_move[0]][current_move[1]]

                #update info table

                board2[1] = info_update( 1, board_dimension, board, board2[1], current_move )
                board2[0] = info_update( 2, board_dimension, board, board2[0], current_move )
                #update move_list


                for d in range(2):
                    for move in range(len(move_list[d%2])):
                        point = score_table[projection(board2[d%2][move_list[d%2][move][0]][move_list[d%2][move][1]])]
                        if point >= move_list[d%2][move][2]:
                            move_list[d%2][move][2] = score_table[projection(board2[d%2][move_list[d%2][move][0]][move_list[d%2][move][1]])]

                for k in range(2):
                    for i in range(3):
                        for j in range(3):
                            w_x = current_move[1]+plus[i][j][1]
                            w_y = current_move[0]+plus[i][j][0]

                            if w_x >= 0 and w_y >= 0 and w_x <= board_dimension-1 and w_y <= board_dimension-1 and board[w_y][w_x] == '.':
                                s = score_table[projection(board2[k%2][w_y][w_x])]

                            lock = 0
                            for item in move_list[k%2]:
                                if item[0] == w_y and item[1] ==  w_x:
                                    lock = 1
                                else:
                                    lock = 0

                            if w_x >= 0 and w_y >= 0 and w_x <= board_dimension-1 and w_y <= board_dimension-1 and board[w_y][w_x] == '.' and [w_y,w_x,s] not in move_list[turn%2] and lock != 1:
                                #print [w_y,w_x,s]
                                move_list[k%2].append([w_y,w_x,s])
                                move_list[k%2] = sorted(move_list[k%2], key=lambda x: x[2] , reverse=True)

                                if len(move_list[k%2]) > size_move_list:
                                   move_list[k%2].pop(size_move_list)

                for s in range(2):
                    temp_list = []
                    for move in move_list[s]:
                        if board[move[0]][move[1]] == '.':
                            temp_list.append(move)
                    move_list[s] = temp_list[:]

                for s in range(2):
                    count = 0
                    temp = []
                    rand_score = move_list[s][0][2]

                    for item in move_list[s]:
                        if item[2] == rand_score:
                            count += 1
                    if count >= 2:
                        move_list[s][0:count] = random.sample(move_list[s][0:count], count)

            #turn alternate and turn is also the total number of stones on the board
            step_history.append([coordinate[0],coordinate[1],turn%2])
            turn += 1

#####################################################################################
#####################################################################################
#MODE 2
    elif mode == '2':
        print 'Which one takes black stone? (1-3)'
        print '1 This Agent.'
        print '2 Random-Agent.'
        print '3 Cancel.'
        order = raw_input()

        if len(order) == 0 or (order != '1' and order != '2' and order != '3'):
            print 'ERROR INFO: invalid input'
            continue

        if order == '1':
            order_num = 1
            print 'this agent takes black stone\n'
        elif order == '2':
            order_num = 0
            print 'this agent takes white stone\n'
        else: #mode == '3':
            print 'CANCELED'
            continue

        #start with follow-moon path
        if order_num == 1:
            yan = int((round(board_dimension-1)/2))
            move_list = [[],[[yan,yan,1000000], [yan-1,yan+1,80000],[yan+1,yan+1,7000]]]

        #generate a list of whole coordinate for random agent

        random_step = []
        for i in range(board_dimension):
            for j in range(board_dimension):
                random_step.append([i,j])

        random_step = random.sample(random_step, len(random_step))
        #print random_step

        while True:
            #show the board on the screen
            show_game(board, board_dimension)

            if game_over(step_history, turn, board, board_dimension, winning_chain_length):
                if turn%2 == 1:
                    print 'white stone win!!'
                    break
                else:
                    print 'black stone win!!'
                    break
            if len(step_history)!= 0:
                print 'last move: %d  %d' %(step_history[len(step_history)-1][0] ,step_history[len(step_history)-1][1])
            print 'turn: %d' %(turn)
            if turn%2 == 1:
                print 'black stone\'s turn'
            else:
                print 'white stone\'s turn'


 ################################################################################################
            if turn%2 == order_num:
                #get coordinate from player
                #start with follow-moon path
                #################################################################################
                #black agent
                if order_num == 1: #take black stone

                    # start with fixed position with good probability to win
                    if turn <= 5:
                        if turn == 5:
                            if board[yan][yan] == 'x' and board[yan-1][yan+1] == 'x':
                                #follow-moon mode
                                if board[yan-1][yan] == 'o' and board[yan][yan+1] == 'o':
                                    current_move = [yan-2, yan+2, 7000]
                                elif board[yan-1][yan] == 'o' and board[yan+1][yan+1] == 'o':
                                    current_move = [yan+1, yan-1, 7000]
                                elif board[yan-1][yan] == 'o' and board[yan+1][yan-1] == 'o':
                                    current_move = [yan-2, yan+1, 7000]
                                else:
                                    current_move = [yan-2, yan+2, 7000]
                                    if board[current_move[0]][current_move[1]] != '.':
                                        current_move = [yan+1, yan-1, 7000]
                                        if board[current_move[0]][current_move[1]] != '.':
                                            current_move = [yan-2, yan+1, 7000]
                                #remove path have been visited
                                temp_item = []
                                for item in move_list[turn%2]:
                                    if item[0] == current_move[0] and item[1] == current_move[1]:
                                        temp_item = item
                                        break
                                if len(temp_item) != 0:
                                    move_list[turn%2].remove(temp_item)

                            else:
                                #glass-moon mode
                                if board[yan-1][yan+1] == 'o' and board[yan-1][yan-1] == 'o':
                                    current_move = [yan, yan+2, 7000]
                                elif board[yan-1][yan+1] == 'o' and board[yan+1][yan] == 'o':
                                    current_move = [yan-1, yan-1, 7000]
                                elif board[yan-1][yan+1] == 'o' and board[yan+2][yan] == 'o':
                                    current_move = [yan-1, yan-1, 7000]
                                else:
                                    current_move = [yan, yan+2, 7000]
                                    if board[current_move[0]][current_move[1]] != '.':
                                        current_move = [yan-1, yan-1, 7000]
                                        if board[current_move[0]][current_move[1]] != '.':
                                          current_move = [yan, yan-1, 7000]
                                #remove path have been visited
                                temp_item = []
                                for item in move_list[turn%2]:
                                    if item[0] == current_move[0] and item[1] == current_move[1]:
                                        temp_item = item
                                        break
                                if len(temp_item) != 0:
                                    move_list[turn%2].remove(temp_item)

                            if [yan+1,yan+1,7000] in move_list[turn%2]:
                                move_list[turn%2].remove([yan+1,yan+1,7000])

                        else:
                            current_move = move_list[turn%2][0]
                            move_list[turn%2].remove(current_move)
                            if board[current_move[0]][current_move[1]] != '.':
                                current_move = move_list[turn%2][0]
                                move_list[turn%2].remove(current_move)

                        # print move_list[turn%2]
                        # print current_move
                        # print board2[turn%2][current_move[0]][current_move[1]]

                        if current_move in move_list[turn%2]:
                            move_list[turn%2].remove(current_move)


                    else:
                        current_move = ab_search(time_limit, move_list, step_history, turn, board, board_dimension, winning_chain_length, board2)

                        # print move_list[turn%2]
                        # print current_move
                        # print board2[turn%2][current_move[0]][current_move[1]]

                        if current_move in move_list[turn%2]:
                            move_list[turn%2].remove(current_move)

                    coordinate[0] = current_move[0]
                    coordinate[1] = current_move[1]

                # coordinate = get_coordinate( board_dimension ,board)
                # current_move = coordinate
                ####################################################################################
                #white agent
                else: #agent take white


                    current_move = ab_search(time_limit, move_list, step_history, turn, board, board_dimension, winning_chain_length, board2)

                    # print move_list[turn%2]
                    # print current_move
                    # print board2[turn%2][current_move[0]][current_move[1]]

                    if current_move in move_list[turn%2]:
                        move_list[turn%2].remove(current_move)

                    coordinate[0] = current_move[0]
                    coordinate[1] = current_move[1]


                if order_num ==1 : #take black stone
                    board[coordinate[0]][coordinate[1]] = 'x'
                else:
                    board[coordinate[0]][coordinate[1]] = 'o'

                random_step.remove([coordinate[0],coordinate[1]])

                #update info table
                board2[1] = info_update( 1, board_dimension, board, board2[1], current_move )
                board2[0] = info_update( 2, board_dimension, board, board2[0], current_move )
                #update move_list


                for d in range(2):
                    for move in range(len(move_list[d%2])):
                        point = score_table[projection(board2[d%2][move_list[d%2][move][0]][move_list[d%2][move][1]])]
                        if point >= move_list[d%2][move][2]:
                            move_list[d%2][move][2] = score_table[projection(board2[d%2][move_list[d%2][move][0]][move_list[d%2][move][1]])]

                for k in range(2):
                    for i in range(3):
                        for j in range(3):
                            w_x = current_move[1]+plus[i][j][1]
                            w_y = current_move[0]+plus[i][j][0]

                            if w_x >= 0 and w_y >= 0 and w_x <= board_dimension-1 and w_y <= board_dimension-1 and board[w_y][w_x] == '.':
                                s = score_table[projection(board2[k%2][w_y][w_x])]

                            lock = 0
                            for item in move_list[k%2]:
                                if item[0] == w_y and item[1] ==  w_x:
                                    lock = 1
                                else:
                                    lock = 0

                            if w_x >= 0 and w_y >= 0 and w_x <= board_dimension-1 and w_y <= board_dimension-1 and board[w_y][w_x] == '.' and [w_y,w_x,s] not in move_list[turn%2] and lock != 1:
                                #print [w_y,w_x,s]
                                move_list[k%2].append([w_y,w_x,s])
                                move_list[k%2] = sorted(move_list[k%2], key=lambda x: x[2] , reverse=True)

                                if len(move_list[k%2]) > size_move_list:
                                   move_list[k%2].pop(size_move_list)


                for s in range(2):
                    temp_list = []
                    for move in move_list[s]:
                        if board[move[0]][move[1]] == '.':
                            temp_list.append(move)
                    move_list[s] = temp_list[:]
                #randomly switch the move in move_list if they have same evaluation
                for s in range(2):
                    count = 0
                    temp = []
                    rand_score = move_list[s][0][2]

                    for item in move_list[s]:
                        if item[2] == rand_score:
                            count += 1
                    if count >= 2:
                        move_list[s][0:count] = random.sample(move_list[s][0:count], count)

            else:
                #put white player

                random.sample(random_step, len(random_step))
                coordinate = random_step.pop(0)
                #get coordinate from agent
                current_move = coordinate
                #update the board

                if order_num ==1 : #take black stone
                    board[coordinate[0]][coordinate[1]] = 'o'
                else:
                    board[coordinate[0]][coordinate[1]] = 'x'

                # print move_list[turn%2]
                # print current_move
                # print board2[turn%2][current_move[0]][current_move[1]]

                #update info table

                board2[1] = info_update( 1, board_dimension, board, board2[1], current_move )
                board2[0] = info_update( 2, board_dimension, board, board2[0], current_move )
                #update move_list


                for d in range(2):
                    for move in range(len(move_list[d%2])):
                        point = score_table[projection(board2[d%2][move_list[d%2][move][0]][move_list[d%2][move][1]])]
                        if point >= move_list[d%2][move][2]:
                            move_list[d%2][move][2] = score_table[projection(board2[d%2][move_list[d%2][move][0]][move_list[d%2][move][1]])]

                for k in range(2):
                    for i in range(3):
                        for j in range(3):
                            w_x = current_move[1]+plus[i][j][1]
                            w_y = current_move[0]+plus[i][j][0]

                            if w_x >= 0 and w_y >= 0 and w_x <= board_dimension-1 and w_y <= board_dimension-1 and board[w_y][w_x] == '.':
                                s = score_table[projection(board2[k%2][w_y][w_x])]

                            lock = 0
                            for item in move_list[k%2]:
                                if item[0] == w_y and item[1] ==  w_x:
                                    lock = 1
                                else:
                                    lock = 0

                            if w_x >= 0 and w_y >= 0 and w_x <= board_dimension-1 and w_y <= board_dimension-1 and board[w_y][w_x] == '.' and [w_y,w_x,s] not in move_list[turn%2] and lock != 1:
                                #print [w_y,w_x,s]
                                move_list[k%2].append([w_y,w_x,s])
                                move_list[k%2] = sorted(move_list[k%2], key=lambda x: x[2] , reverse=True)

                                if len(move_list[k%2]) > size_move_list:
                                   move_list[k%2].pop(size_move_list)

                for s in range(2):
                    temp_list = []
                    for move in move_list[s]:
                        if board[move[0]][move[1]] == '.':
                            temp_list.append(move)
                    move_list[s] = temp_list[:]

                for s in range(2):
                    count = 0
                    temp = []
                    rand_score = move_list[s][0][2]

                    for item in move_list[s]:
                        if item[2] == rand_score:
                            count += 1
                    if count >= 2:
                        move_list[s][0:count] = random.sample(move_list[s][0:count], count)

            #turn alternate and turn is also the total number of stones on the board
            step_history.append([coordinate[0],coordinate[1],turn%2])
            turn += 1

#####################################################################################
#####################################################################################
#MODE 3
    else: #mode == '1'

        order_num = 1

        #start with follow-moon path
        if order_num == 1:
            yan = int((round(board_dimension-1)/2))
            move_list = [[],[[yan,yan,1000000], [yan-1,yan+1,80000],[yan+1,yan+1,7000]]]

        while True:
            #show the board on the screen
            show_game(board, board_dimension)

            if game_over(step_history, turn, board, board_dimension, winning_chain_length):
                if turn%2 == 1:
                    print 'white stone win!!'
                    break
                else:
                    print 'black stone win!!'
                    break
            if len(step_history)!= 0:
                print 'last move: %d  %d' %(step_history[len(step_history)-1][0] ,step_history[len(step_history)-1][1])
            print 'turn: %d' %(turn)
            if turn%2 == 1:
                print 'black stone\'s turn'
            else:
                print 'white stone\'s turn'


 ################################################################################################
            if turn%2 == order_num:
                #get coordinate from player
                #start with follow-moon path
                #################################################################################
                #black agent
                if order_num == 1: #take black stone

                    # start with fixed position with good probability to win
                    if turn <= 5:
                        if turn == 5:
                            if board[yan][yan] == 'x' and board[yan-1][yan+1] == 'x':
                                #follow-moon mode
                                if board[yan-1][yan] == 'o' and board[yan][yan+1] == 'o':
                                    current_move = [yan-2, yan+2, 7000]
                                elif board[yan-1][yan] == 'o' and board[yan+1][yan+1] == 'o':
                                    current_move = [yan+1, yan-1, 7000]
                                elif board[yan-1][yan] == 'o' and board[yan+1][yan-1] == 'o':
                                    current_move = [yan-2, yan+1, 7000]
                                else:
                                    current_move = [yan-2, yan+2, 7000]
                                    if board[current_move[0]][current_move[1]] != '.':
                                        current_move = [yan+1, yan-1, 7000]
                                        if board[current_move[0]][current_move[1]] != '.':
                                            current_move = [yan-2, yan+1, 7000]
                                #remove path have been visited
                                temp_item = []
                                for item in move_list[turn%2]:
                                    if item[0] == current_move[0] and item[1] == current_move[1]:
                                        temp_item = item
                                        break
                                if len(temp_item) != 0:
                                    move_list[turn%2].remove(temp_item)

                            else:
                                #glass-moon mode
                                if board[yan-1][yan+1] == 'o' and board[yan-1][yan-1] == 'o':
                                    current_move = [yan, yan+2, 7000]
                                elif board[yan-1][yan+1] == 'o' and board[yan+1][yan] == 'o':
                                    current_move = [yan-1, yan-1, 7000]
                                elif board[yan-1][yan+1] == 'o' and board[yan+2][yan] == 'o':
                                    current_move = [yan-1, yan-1, 7000]
                                else:
                                    current_move = [yan, yan+2, 7000]
                                    if board[current_move[0]][current_move[1]] != '.':
                                        current_move = [yan-1, yan-1, 7000]
                                        if board[current_move[0]][current_move[1]] != '.':
                                          current_move = [yan, yan-1, 7000]
                                #remove path have been visited
                                temp_item = []
                                for item in move_list[turn%2]:
                                    if item[0] == current_move[0] and item[1] == current_move[1]:
                                        temp_item = item
                                        break
                                if len(temp_item) != 0:
                                    move_list[turn%2].remove(temp_item)

                            if [yan+1,yan+1,7000] in move_list[turn%2]:
                                move_list[turn%2].remove([yan+1,yan+1,7000])

                        else:
                            current_move = move_list[turn%2][0]
                            move_list[turn%2].remove(current_move)
                            if board[current_move[0]][current_move[1]] != '.':
                                current_move = move_list[turn%2][0]
                                move_list[turn%2].remove(current_move)
                        #print infomation
                        # print move_list[turn%2]
                        # print current_move
                        # print board2[turn%2][current_move[0]][current_move[1]]

                        if current_move in move_list[turn%2]:
                            move_list[turn%2].remove(current_move)


                    else:
                        current_move = ab_search(time_limit, move_list, step_history, turn, board, board_dimension, winning_chain_length, board2)

                        #print information
                        # print move_list[turn%2]
                        # print current_move
                        # print board2[turn%2][current_move[0]][current_move[1]]

                        if current_move in move_list[turn%2]:
                            move_list[turn%2].remove(current_move)

                    coordinate[0] = current_move[0]
                    coordinate[1] = current_move[1]


                board[coordinate[0]][coordinate[1]] = 'x'

                #update info table
                board2[1] = info_update( 1, board_dimension, board, board2[1], current_move )
                board2[0] = info_update( 2, board_dimension, board, board2[0], current_move )
                #update move_list


                for d in range(2):
                    for move in range(len(move_list[d%2])):
                        point = score_table[projection(board2[d%2][move_list[d%2][move][0]][move_list[d%2][move][1]])]
                        if point >= move_list[d%2][move][2]:
                            move_list[d%2][move][2] = score_table[projection(board2[d%2][move_list[d%2][move][0]][move_list[d%2][move][1]])]

                for k in range(2):
                    for i in range(3):
                        for j in range(3):
                            w_x = current_move[1]+plus[i][j][1]
                            w_y = current_move[0]+plus[i][j][0]

                            if w_x >= 0 and w_y >= 0 and w_x <= board_dimension-1 and w_y <= board_dimension-1 and board[w_y][w_x] == '.':
                                s = score_table[projection(board2[k%2][w_y][w_x])]

                            lock = 0
                            for item in move_list[k%2]:
                                if item[0] == w_y and item[1] ==  w_x:
                                    lock = 1
                                else:
                                    lock = 0

                            if w_x >= 0 and w_y >= 0 and w_x <= board_dimension-1 and w_y <= board_dimension-1 and board[w_y][w_x] == '.' and [w_y,w_x,s] not in move_list[turn%2] and lock != 1:
                                #print [w_y,w_x,s]
                                move_list[k%2].append([w_y,w_x,s])
                                move_list[k%2] = sorted(move_list[k%2], key=lambda x: x[2] , reverse=True)

                                if len(move_list[k%2]) > size_move_list:
                                   move_list[k%2].pop(size_move_list)


                for s in range(2):
                    temp_list = []
                    for move in move_list[s]:
                        if board[move[0]][move[1]] == '.':
                            temp_list.append(move)
                    move_list[s] = temp_list[:]
                #randomly switch the move in move_list if they have same evaluation
                for s in range(2):
                    count = 0
                    temp = []
                    rand_score = move_list[s][0][2]

                    for item in move_list[s]:
                        if item[2] == rand_score:
                            count += 1
                    if count >= 2:
                        move_list[s][0:count] = random.sample(move_list[s][0:count], count)

            else:
                #put white player


                current_move = ab_search(time_limit, move_list, step_history, turn, board, board_dimension, winning_chain_length, board2)

                print move_list[turn%2]
                print current_move
                print board2[turn%2][current_move[0]][current_move[1]]

                if current_move in move_list[turn%2]:
                    move_list[turn%2].remove(current_move)

                coordinate[0] = current_move[0]
                coordinate[1] = current_move[1]

                board[coordinate[0]][coordinate[1]] = 'o'

                #pritn information
                # print move_list[turn%2]
                # print current_move
                # print board2[turn%2][current_move[0]][current_move[1]]

                #update info table

                board2[1] = info_update( 1, board_dimension, board, board2[1], current_move )
                board2[0] = info_update( 2, board_dimension, board, board2[0], current_move )
                #update move_list


                for d in range(2):
                    for move in range(len(move_list[d%2])):
                        point = score_table[projection(board2[d%2][move_list[d%2][move][0]][move_list[d%2][move][1]])]
                        if point >= move_list[d%2][move][2]:
                            move_list[d%2][move][2] = score_table[projection(board2[d%2][move_list[d%2][move][0]][move_list[d%2][move][1]])]

                for k in range(2):
                    for i in range(3):
                        for j in range(3):
                            w_x = current_move[1]+plus[i][j][1]
                            w_y = current_move[0]+plus[i][j][0]

                            if w_x >= 0 and w_y >= 0 and w_x <= board_dimension-1 and w_y <= board_dimension-1 and board[w_y][w_x] == '.':
                                s = score_table[projection(board2[k%2][w_y][w_x])]

                            lock = 0
                            for item in move_list[k%2]:
                                if item[0] == w_y and item[1] ==  w_x:
                                    lock = 1
                                else:
                                    lock = 0

                            if w_x >= 0 and w_y >= 0 and w_x <= board_dimension-1 and w_y <= board_dimension-1 and board[w_y][w_x] == '.' and [w_y,w_x,s] not in move_list[turn%2] and lock != 1:
                                #print [w_y,w_x,s]
                                move_list[k%2].append([w_y,w_x,s])
                                move_list[k%2] = sorted(move_list[k%2], key=lambda x: x[2] , reverse=True)

                                if len(move_list[k%2]) > size_move_list:
                                   move_list[k%2].pop(size_move_list)

                for s in range(2):
                    temp_list = []
                    for move in move_list[s]:
                        if board[move[0]][move[1]] == '.':
                            temp_list.append(move)
                    move_list[s] = temp_list[:]

                for s in range(2):
                    count = 0
                    temp = []
                    rand_score = move_list[s][0][2]

                    for item in move_list[s]:
                        if item[2] == rand_score:
                            count += 1
                    if count >= 2:
                        move_list[s][0:count] = random.sample(move_list[s][0:count], count)

            #turn alternate and turn is also the total number of stones on the board
            step_history.append([coordinate[0],coordinate[1],turn%2])
            turn += 1
