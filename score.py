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
import pdb 
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
                (1,1,0,1,0): 'l_3',
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
                (2,2,0,2,0): 'b_3',
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
@jit
def score(board,witdh,nplayer):

    pat_l = []
    boardrot = np.rot90(board)
    psize = 5
    ret = 0

    for x in xrange(0, witdh):
        for y in xrange(0, witdh - psize + 1):
            a = tuple(board[x:x + 1, y:y + psize].flatten())
            b = tuple(board[y:y + psize, x:x + 1].flatten())

            if a in type_table:
                pat_l.append(type_table[a]) 
                ret += score_table[type_table[a]]
            if b in type_table:
                pat_l.append(type_table[b]) 
                ret += score_table[type_table[b]]

    for x in xrange(-witdh, witdh):
        for y in xrange(0, witdh - psize + 1):
            a = tuple(board.diagonal(x)[y:y+psize])
            b = tuple(boardrot.diagonal(x)[y:y+psize])
            if a in type_table:
                ret += score_table[type_table[a]]
                pat_l.append(type_table[a]) 
            if b in type_table:
                ret += score_table[type_table[b]]
                pat_l.append(type_table[b]) 
    if nplayer == 1:
        return ret
    else:
        return -ret
@jit
def computescore(board,width,nplayer,xmov,ymov): # spocitam hvezdici patternu 10*10 s novym uprostred a bez nej
# a pak odectu starou a prictu novou
    board = board
    newPatt = []
    boardrot = np.rot90(board)
    psize = 5
    ret = 0


    c = tuple(board.diagonal(-xmov+ymov))
    d = tuple(boardrot.diagonal(-width+1+ymov+xmov))
    a = tuple(board[xmov:xmov + 1].flatten())
    b = tuple(boardrot[-ymov-1].flatten())
    # if (board == x).all():
    #    pdb.set_trace()  # breakpoint 7a891b19 //
 
    for x in xrange(0,len(a)-psize+1):
        aa = tuple(a[x:x+psize])
        if aa in type_table:
            newPatt.append(type_table[aa]) 
            ret += score_table[type_table[aa]]

    for x in xrange(0,len(b)-psize+1):
        bb = tuple(b[x:x+psize])
        if bb in type_table:
            newPatt.append(type_table[bb]) 
            ret += score_table[type_table[bb]]

    for x in xrange(0,len(c)-psize+1):
        cc = tuple(c[x:x+psize])
        if cc in type_table:
            newPatt.append(type_table[cc]) 
            ret += score_table[type_table[cc]]

    for x in xrange(0,len(d)-psize+1):
        dd = tuple(d[x:x+psize])
        if dd in type_table:
            newPatt.append(type_table[dd]) 
            ret += score_table[type_table[dd]]


    return ret

