from __future__ import print_function
import random
from pprint import pprint
import pipe as pp
from pipe import DEBUG_EVAL, DEBUG
import sys
import numpy as np
from decimal import *

class ai():
    def __init__(self): # empty init, not insert anything
        return None

    def isFree(self,x, y): # check if x/y cell is free
        return x >= 0 and y >= 0 and x < self.width and y < self.width and self.board[x][y] == 0

    def init(self,width): # called at start of game
        getcontext().prec = 3
        self.width = width
        self.weights_width = 7

        self.board = [[0 for i in xrange(width)] for j in xrange(width)]
        self.generatemy(self.weights_width)
        self.generateopp(self.weights_width)
        self.generateinit(width)
        self.weight_board = self.init_weigth[:]

    def generatemy(self,width): # my matrix, star
        self.pl_weight_board = [[0 for i in xrange(width)] for j in xrange(width)]
        for x in range(width):
            for y in range(width):
                if x==width/2 or y==width/2 or x + y == width -1 or abs(x) == abs(y): # funguje jen na ctvrecich
                    self.pl_weight_board[x][y] = - self.weights_width / (1+ max(abs(x-width/2) , abs(y-width/2)))
                    # self.pl_weight_board[x][y] = -1.0/(1+abs(x-width/2)) - 1.0/(1+abs(y-width/2))
        self.pl_weight_board = np.around(self.pl_weight_board, decimals=1)
        # print("player")
        # pprint(self.pl_weight_board)

    def generateopp(self,width):
        self.opp_weight_board =  [[0 for i in xrange(width)] for j in xrange(width)]
        for x in range(width):
            for y in range(width):
                if x==width/2 or y==width/2 or x + y == width -1 or abs(x) == abs(y): # funguje jen na ctvrecich
                    self.opp_weight_board[x][y] = self.weights_width /(1+ max(abs(x-width/2) , abs(y-width/2)))
                    # self.opp_weight_board[x][y] = -1.0/(abs(x-width/2)+1) -1.0/(1+abs(y-width/2))
        self.opp_weight_board = np.around(self.opp_weight_board, decimals=1)

    def generateinit(self,width):
        self.init_weigth =  [[0 for i in xrange(width)] for j in xrange(width)]
        for x in range(self.width):
            for y in range(self.width):
                self.init_weigth[x][y] = abs(x-width/2) + abs(y-width/2)
        self.init_weigth = np.around(self.init_weigth, decimals=1)

    def my(self,x,y): # add your turn to internal data structure
        # print("BEFORE" + str(x) + ":" + str(y))
        # pprint(self.weight_board)
        self.board[x][y] = 1
        self.merge_weights(x,y,self.pl_weight_board)
        # print("AFTER" + str(x) + ":" + str(y))
        # pprint(self.weight_board)

    def opp(self,x,y): #add opponent turn to internal data structure
        self.board[x][y] = 2
        self.merge_weights(x,y,self.opp_weight_board)
        # pprint(self.weight_board)

    def merge_weights(self,x,y,weights):
        for xw in range(self.width):
            for yw in range(self.width):
                shiftx = xw-x
                shifty = yw-y
                if    ( abs(shiftx) > self.weights_width/2 or abs(shifty) > self.weights_width/2 ):
                    continue
                # print(str(shiftx) + ":" + str(shifty))
                self.weight_board[xw][yw] += weights[self.weights_width/2 + shiftx][self.weights_width/2 + shifty]

    def turn(self): # play your turn and add it to your internal data structure
        if pp.terminateAI:
            return
        maxx,maxy = 0,0
        val = self.weight_board[0][0]
        for x in range(self.width):
            for y in range(self.width):
                if self.isFree(x,y):
                    if self.weight_board[x][y]<val:
                        val = self.weight_board[x][y]
                        maxx = x
                        maxy = y
        return maxx,maxy


        # if i > 1:
        #     pp.pipeOut("DEBUG {} coordinates didn't hit an empty field".format(i))
        # pass
        #  C:\Python27\Scripts\pyinstaller.exe main.py pipe.py aiweight.py --name pbrain-sim.exe --onefile