from __future__ import print_function
from pprint import pprint
import random
import pipe as P
import numpy as np
from pipe import DEBUG_EVAL, DEBUG
import sys
from easyAI import TwoPlayersGame, Human_Player, AI_Player, Negamax
from easyAI import id_solve, TT
import numpy as np
from easyAI import SSS

FREE = 0
type_table = {
                (1,1,1,1,1): 'l_5',

                (1,1,1,1,0): 'l_4c',
                (1,1,1,0,1): 'l_4',
                (1,1,0,1,1): 'l_4',
                (1,0,1,1,1): 'l_4',
                (0,1,1,1,1): 'l_4c',

                (0,0,1,1,1): 'l_3c',
                (0,1,0,1,1): 'l_3',
                (0,1,1,0,1): 'l_3',
                (0,1,1,1,0): 'l_3c',
                (1,0,0,1,1): 'l_3',
                (1,0,1,0,1): 'l_3',
                (1,0,1,1,0): 'l_3',
                (1,1,0,0,1): 'l_3',
                (1,1,1,0,0): 'l_3c',

                (1,1,0,0,0): 'l_2c',
                (1,0,1,0,0): 'l_2',
                (1,0,0,1,0): 'l_2',
                (1,0,0,0,1): 'l_2',
                (0,1,1,0,0): 'l_2c',
                (0,1,0,1,0): 'l_2',
                (0,1,0,0,1): 'l_2',
                (0,0,1,1,0): 'l_2c',
                (0,0,1,0,1): 'l_2',
                (0,0,0,1,1): 'l_2c',

# ENEMY
                (2,2,2,2,2): 'b_5',

                (2,2,2,2,0): 'b_4c',
                (2,2,2,0,2): 'b_4',
                (2,2,0,2,2): 'b_4',
                (2,0,2,2,2): 'b_4',
                (0,2,2,2,2): 'b_4c',

                (0,0,2,2,2): 'b_3c',
                (0,2,0,2,2): 'b_3',
                (0,2,2,0,2): 'b_3',
                (0,2,2,2,0): 'b_3c',
                (2,0,0,2,2): 'b_3',
                (2,0,2,0,2): 'b_3',
                (2,0,2,2,0): 'b_3',
                (2,2,0,0,2): 'b_3',
                (2,2,2,0,0): 'b_3c',

                (2,2,0,0,0): 'b_2c',
                (2,0,2,0,0): 'b_2',
                (2,0,0,2,0): 'b_2',
                (2,0,0,0,2): 'b_2',
                (0,2,2,0,0): 'b_2c',
                (0,2,0,2,0): 'b_2',
                (0,2,0,0,2): 'b_2',
                (0,0,2,2,0): 'b_2c',
                (0,0,2,0,2): 'b_2',
                (0,0,0,2,2): 'b_2c'
             }

score_table = {
                'b_5':-1000000,
                'b_4c':-100000,
                'b_4':  -10000,
                'b_3c':  -1000,
                'b_3':    -100,
                'b_2c':    -10,
                'b_2':      -1,

                'l_5': 1000000,
                'l_4c': 100000,
                'l_4':   10000,
                'l_3c':   1000,
                'l_3':     100,
                'l_2c':     10,
                'l_2':       1,

                'z':         0
             }


class GomokuGame(TwoPlayersGame):
    """ Gomoku game for minimax """

    def __init__(self, players, width):
        self.players = players
        self.width = width
        self.board = np.zeros((width, width), np.int8)
        self.board[width/2][width/2] = 2
        # self.board[width/2][width/2+1] = 2
        self.hboard = tuple(map(tuple, self.board))
        self.nplayer = 1  # player 1 starts

    def htob(self):
        self.board = np.asarray(self.hboard)


    def spot_string(self, i, j):
        return ["_", "O", "X"][self.board[j][i]]

    def possible_moves(self):
        ret = []
        rng = 1
        for x in xrange(0, self.width):
            for y in xrange(0, self.width): # for all cells in grid
                if self.board[x][y] == FREE: # if the cell is free
                    for xx in xrange(max(0,x-rng),min(x+rng+1,self.width)):
                        for yy in xrange(max(0,y-rng),min(y+rng+1,self.width)):
                            if self.board[xx][yy] != 0: # check neighbours 
                                ret.append([x, y])
        return ret


    def make_move(self, move):
        self.board[move[0], move[1]] = self.nplayer
        self.hboard = tuple(map(tuple, self.board))

    def unmake_move(self, move):
        self.board[move[0], move[1]] = 0
        self.hboard = tuple(map(tuple, self.board))

    def win(self):
        return self.checkwin(self.nplayer)

    def loose(self):
        return self.checkwin(self.nopponent)

    def winner(self):
        if self.checkwin(2):
            return "Vyhrava AI"
        if self.checkwin(1):
            return "Vyhravas ty"
        return "buhvi"


    def checkwin(self, pl):
        me = pl
        five = np.array([me, me, me, me, me], np.int8)
        psize = 5
        boardrot = np.rot90(self.board)
        for x in xrange(0, self.width):
            for y in xrange(0, self.width - psize + 1):
                a = (self.board[x:x + 1, y:y + psize].flatten())
                b = (self.board[y:y + psize, x:x + 1].flatten())
                if self.samearray(a, five):
                    return True
                if self.samearray(b, five):
                    return True
        for x in xrange(-self.width, self.width):
            if self.samearray(self.board.diagonal(x)[:psize], five):
                return True
            if self.samearray(boardrot.diagonal(x)[:psize], five):
                return True
        return False

    # Game stops when someone wins.
    def is_over(self): return self.win() or self.loose() or (self.possible_moves == [])

    def show(self): pprint(self.board)

    def samearray(self,a,b):
        aa = len(a)
        bb = len(b)
        if aa != bb:
            return False
        for x in xrange(0,aa):
            if a[x] != b[x]:
                return False
        return True


    def ttentry(self):
        return "".join([".0X"[i] for i in self.board.flatten()])

    def scoring(self):

        pat_l = []
        boardrot = np.rot90(self.board)
        psize = 5
        ret = 0

        for x in xrange(0, self.width):
            for y in xrange(0, self.width - psize + 1):
                a = tuple(self.board[x:x + 1, y:y + psize].flatten())
                b = tuple(self.board[y:y + psize, x:x + 1].flatten())

                if a in type_table:
                    pat_l.append(type_table[a]) 
                    ret += score_table[type_table[a]]
                if b in type_table:
                    pat_l.append(type_table[b]) 
                    ret += score_table[type_table[b]]

        for x in xrange(-self.width, self.width):
            for y in xrange(0, self.width - psize + 1):
                a = tuple(self.board.diagonal(x)[y:y+psize])
                b = tuple(boardrot.diagonal(x)[y:y+psize])
                if a in type_table:
                    ret += score_table[type_table[a]]
                    pat_l.append(type_table[a]) 
                if b in type_table:
                    ret += score_table[type_table[b]]
                    pat_l.append(type_table[b]) 

        # ret = score_table[self.projection(pat_l)]
        # print(str(ret))
        # for x in pat_l:
            

        if self.nplayer == 1:
            return ret
        else:
            return -ret

    def projection(self,type_list):

        if type_list.count('l_5') >= 1:
            return 'l_5'
        elif type_list.count('l_4') >= 1:
            return 'l_4'
        elif type_list.count('l_3') >= 1:
            return 'l_3'
        elif type_list.count('l_2') >= 1:
            return 'l_2'
        else:
            return 'z'


# tt = TT()
# ai = Negamax(4, win_score = 90000 )
# GomokuGame.ttentry = lambda game : game.hboard 
# game = GomokuGame([AI_Player(ai), Human_Player()], 6)
# id_solve( game, ai_depths=range(2,10), win_score=80000, tt=tt)
# print(str(r) + ":" + str(d) + ":" + str(m))
# game.play()  # you will always lose this game :)
