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
from score import computescore,type_table,score_table

FREE = 0

class GomokuGame(TwoPlayersGame):
    """ Gomoku game for minimax """

    def __init__(self, players, width):
        self.players = players
        self.width = width
        self.board = np.zeros((width, width), np.int8)
        # self.board[width/2][width/2] = 2
        self.hboard = tuple(map(tuple, self.board))
        self.nplayer = 1  # player 1 starts
        self.movecount = 1  # player 1 starts
        self.score = 0  
        self.oldPatt = []
        self.DBG = False

    def htob(self):
        self.board = np.asarray(self.hboard)
        self.score = self.scorefromscratch()

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
            ret.append([width/2,width/2])
        return ret

    def scoring(self):
        sc = self.score
        ss = self.scorefromscratch()
        if sc != -ss:
            import pdb; pdb.set_trace()  # breakpoint 69cb5e3d //       board = self.board

        return -self.score

    def make_move(self, move):
        nplayer = self.nplayer
        oldscore = self.score
        self.df = False
        self.movecount += 1
        self.last = self.nplayer
        scorediff = computescore(self.board,self.width,self.nplayer,move[0],(move[1]))
        self.board[move[0], move[1]] = self.nplayer
        self.df = True
        scorediff2 = computescore(self.board,self.width,self.nplayer,int(move[0]),int(move[1]))
        self.hboard = tuple(map(tuple, self.board))
        board = self.board
        diff = scorediff2 - scorediff
        if self.nplayer == 1:
            self.score = -1 * self.score
            self.score += diff ## musi byt plus
        else:
            self.score = -1 * self.score
            self.score -= diff ## musi byt minus


        # def unmake_move(self, move):
        #     player = self.board[move[0],move[1]]
        #     oldscore = self.score
        #     # if self.nplayer == 1: ## MUSI platit i pro dvojku
        #     self.score = -1 * self.score

        #     scorediff = computescore(self.board,self.width,self.nplayer,move[0],(move[1]))
        #     self.board[move[0], move[1]] = 0
        #     scorediff2 = computescore(self.board,self.width,self.nplayer,int(move[0]),int(move[1]))
        #     self.hboard = tuple(map(tuple, self.board))
        #     self.score += scorediff -scorediff2
        #     sc = self.score
        #     ss = self.scorefromscratch()
        #     if sc != ss:
        #         import pdb; pdb.set_trace()  # breakpoint 69cb5e3d //

        #     board = self.board



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



    def scorefromscratch(self):

        pat_l = []
        boardrot = np.rot90(self.board)
        psize = 5
        ret = 0

        for x in xrange(0, self.width):
            for y in xrange(0, self.width - psize + 1):
                a = tuple(self.board[x:x + 1, y:y + psize].flatten())
                b = tuple(self.board[y:y + psize, x:x + 1].flatten())

                if a in type_table:
                    if self.DBG:
                        import pdb; pdb.set_trace()  # breakpoint 6774a74d //
                    pat_l.append(type_table[a]) 
                    ret += score_table[type_table[a]]
                if b in type_table:
                    if self.DBG:
                        import pdb; pdb.set_trace()  # breakpoint 6774a74d //
                    pat_l.append(type_table[b]) 
                    ret += score_table[type_table[b]]

        for x in xrange(-self.width, self.width):
            for y in xrange(0, self.width - psize + 1):
                a = tuple(self.board.diagonal(x)[y:y+psize])
                b = tuple(boardrot.diagonal(x)[y:y+psize])
                if a in type_table:
                    if self.DBG:
                        import pdb; pdb.set_trace()  # breakpoint 6774a74d //
                    ret += score_table[type_table[a]]
                    pat_l.append(type_table[a]) 
                if b in type_table:
                    if self.DBG:
                        import pdb; pdb.set_trace()  # breakpoint 6774a74d //
                    ret += score_table[type_table[b]]
                    pat_l.append(type_table[b]) 
        if self.nplayer == 1:
            return ret
        else:
            return -ret