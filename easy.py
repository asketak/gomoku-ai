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
                '00022': 'l_1',
                '00202': 'l_1',
                '00220': 'b_2',
                '00222': 'b_3',
                '02002': 'l_1',
                '02020': 'l_1',
                '02022': 'b_3',
                '02200': 'b_2',
                '02202': 'b_3',
                '02220': 'b_3',
                '02222': 'b_4',
                '22000': 'l_1',
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
                '00001': 'l_1',
                '00221': 'l_1',
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
                '20010': 'l_1',
                '20210': 'l_1',
                '22010': 'l_1',
                '00010': 'l_1',
                '00011': 'b_2',
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
                '01000': 'l_1',
                '01001': 'l_2',
                '21001': 'b_2',
                '01010': 'l_2',
                '21010': 'b_2',
                '01011': 'l_3',
                '21011': 'b_3',
                '01101': 'l_3',
                '21101': 'b_3',
                '01110': 'l_3',
                '21110': 'b_3',
                '01112': 'b_3',
                '01111': 'l_4',
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
                '11220': 'b_2',
                '11202': 'b_2',
                '11222': 'b_2',
                '11001': 'l_3',
                '11010': 'l_3',
                '11012': 'b_3',
                '11011': 'l_4',
                '11100': 'b_3',
                '11102': 'b_3',
                '11101': 'l_4',
                '11110': 'l_4',
                '11112': 'b_4'
             }

score_table = {'l_5': 100000,
                'l_4': 10000,
                'db_4': 10000,
                'b4_l3': 10000,
                'dl_3': 5000,
                'b3_l3': 1000,
                'b_4': 500,
                'l_3': 200,
                'db_3': 100,
                'b_3': 50,
                'dl_2': 10,
                'l_2': 5,
                'b_2': 3,
                'l_1': 1,
                'z': 0
             }


class GomokuGame(TwoPlayersGame):
    """ Gomoku game for minimax """

    def __init__(self, players, width):
        self.players = players
        self.width = width
        self.board = np.zeros((width, width), np.int8)
        # self.hboard = tuple(map(tuple, self.board))
        self.nplayer = 1  # player 1 starts

    def possible_moves(self):
        ret = []
        for x in xrange(0, self.width):
            for y in xrange(0, self.width):
                if self.board[x][y] == FREE:
                    ret.append([x, y])
        return ret

    def make_move(self, move):
        self.board[move[0], move[1]] = self.nplayer
        # self.hboard = tuple(map(tuple, self.board))

    def unmake_move(self, move):
        self.board[move[0], move[1]] = 0
        # self.hboard = tuple(map(tuple, self.board))

    def win(self):
        return self.checkwin(self.nplayer)

    def loose(self):
        return self.checkwin(self.nopponent)

    def checkwin(self, pl):
        me = pl
        five = np.array([me, me, me, me, me], np.int8)
        psize = 5
        for x in xrange(0, self.width):
            for y in xrange(0, self.width - psize + 1):
                a = (self.board[x:x + 1, y:y + psize].flatten())
                b = (self.board[y:y + psize, x:x + 1].flatten())
                if np.array_equal(a, five):
                    return True
                if np.array_equal(b, five):
                    return True
        for x in xrange(-self.width, self.width):
            if np.array_equal(self.board.diagonal(x)[:psize], five):
                return True
            if np.array_equal(np.rot90(self.board).diagonal(x)[:psize], five):
                return True
        return False

    # Game stops when someone wins.
    def is_over(self): return self.win() or self.loose()

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


    def scoring(self):
        if self.loose():
            return -100000
        if self.win():
            return 100000

        pat_l = []
        boardrot = np.rot90(self.board)

    for patt in type_table:
        patt_str = type_table[patt]
        
        patt  = list(patt)
        psize = len(patt)
        patt  = np.asarray(patt, np.int8)

        for x in xrange(0, self.width):
            for y in xrange(0, self.width - psize + 1):
                a = (self.board[x:x + 1, y:y + psize].flatten())
                b = (self.board[y:y + psize, x:x + 1].flatten())
                if self.samearray(a, patt):
                    pat_l.append(patt_str) 
                if self.samearray(b, patt):
                    pat_l.append(patt_str) 

        for x in xrange(-self.width, self.width):
            for y in xrange(0, self.width - psize + 1):
                if self.samearray(self.board.diagonal(x)[y:y+psize], patt):
                    pat_l.append(patt_str) 
                if self.samearray(boardrot.diagonal(x)[y:y+psize], patt):
                    pat_l.append(patt_str) 

        ret = score_table[self.projection(pat_l)]

        if self.nplayer == 1:
            return ret
        else:
            return -ret


    def projection(self,type_list):

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



ai = Negamax(5)
# tt = TT()
# GomokuGame.ttentry = lambda game : game.hboard 
game = GomokuGame([AI_Player(ai), Human_Player()], 5)
# r,d,m = id_solve( game, ai_depths=range(2,10), win_score=80000, tt=tt)
# print(str(r) + ":" + str(d) + ":" + str(m))
game.play()  # you will always lose this game :)
