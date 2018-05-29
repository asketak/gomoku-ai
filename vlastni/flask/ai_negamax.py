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
from numba import jit
from score import score


FREE = 0

# This recomputes whole board each turn

class GomokuGame(TwoPlayersGame):
    """ Gomoku game for minimax """

    def __init__(self, players, width,player):
        self.players = players
        self.width = width
        self.board = np.zeros((width, width), np.int8)
        # self.board[width/2][width/2] = 2
        self.hboard = tuple(map(tuple, self.board))
        self.nplayer = player  # player 1 starts

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
                    for xx in xrange(max(0,x-rng),min(x+rng+1,self.width)): # for all cells nearby
                        for yy in xrange(max(0,y-rng),min(y+rng+1,self.width)): # for all cells nearby
                            if self.board[xx][yy] != 0: # check neighbours 
                                ret.append([x, y])
        if ret == []:
            ret.append([self.width/2,self.width/2])
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

    def ttentry(self):
        return self.hboard;

    def checkwin(self,pl):
        me = pl

        pat_l = []
        five = np.array([me, me, me, me, me], np.int8)
        boardrot = np.rot90(self.board)
        psize = 5
        ret = 0

        for x in xrange(0, self.width):
            for y in xrange(0, self.width - psize + 1):
                a = tuple(self.board[x:x + 1, y:y + psize].flatten())
                b = tuple(self.board[y:y + psize, x:x + 1].flatten())
                if self.samearray(a,five):
                    return True
                if self.samearray(b,five):
                    return True

        for x in xrange(-self.width, self.width):
            for y in xrange(0, self.width - psize + 1):
                a = tuple(self.board.diagonal(x)[y:y+psize])
                b = tuple(boardrot.diagonal(x)[y:y+psize])
                if self.samearray(a,five):
                    return True
                if self.samearray(b,five):
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
    # def ttrestore(self,entry}
        

    def scoring(self):
        return score(self.board,self.width,self.nplayer)

