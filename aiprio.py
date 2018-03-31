from __future__ import print_function
from Print import Print
import random
import pipe as P
import numpy as np
from pipe import DEBUG_EVAL, DEBUG
import sys

PLAYER = 8
OPONENT = 4
FREE = 2
X = 3

PATT1 = [[FREE,PLAYER,PLAYER,OPONENT]]
PATT2 = [[FREE,PLAYER,PLAYER,FREE]]
PATT3 = [[OPONENT,PLAYER,PLAYER,PLAYER,FREE]]
PATT4 = [[PLAYER,PLAYER],
         [ANY,PLAYER]]
PATT5 = [[PLAYER,PLAYER,PLAYER,PLAYER,OPONENT]]
PATT6 = [[FREE,PLAYER,PLAYER,PLAYER,FREE]]
PATT8 = [[PLAYER,PLAYER,PLAYER,FREE],
         [ANY   ,ANY   ,PLAYER,ANY ],
         [ANY   ,ANY   ,PLAYER,ANY ],
         [ANY   ,ANY   ,FREE  ,ANY ]]
PATT82 =[[ANY ,ANY   ,ANY   ,ANY   ,FREE],
         [FREE,PLAYER,PLAYER,PLAYER,FREE],
         [ANY ,ANY   ,PLAYER,ANY   ,ANY ],
         [ANY ,PLAYER,ANY   ,ANY   ,ANY ],
         [FREE,ANY   ,ANY   ,ANY   ,ANY ]]
         
PATT9 = [[FREE,PLAYER,PLAYER,PLAYER,PLAYER,FREE]]
PATT6 = [[FREE,PLAYER,PLAYER,PLAYER,FREE]]




class ai():
    def __init__(self): # empty init, not insert anything
        return None

    def isFree(self,x, y): # check if x/y cell is free
        return x >= 0 and y >= 0 and x < self.width and y < self.width and self.board[x][y] == FREE

    def init(self,width): # called at start of game
        self.width = width
        # self.board = np.full((self.width, self.width), FREE)
        self.board = np.arange(400).reshape(20, 20)

    def my(self,x,y): # add your turn to internal data structure
        self.board[x][y] = PLAYER

    def opp(self,x,y): #add oPonent turn to itnernal data structure
        self.board[x][y] = OPONENT

    def compare(self,board,pattern):
        xsize = len(pattern[0])
        ysize = len(pattern)
        for y in xrange(0,ysize):
            for x in xrange(0,xsize):

    def find_pattern(self,player,enemy,pattern):
        xsize = len(pattern[0])
        ysize = len(pattern)

        for y in xrange(0,self.width-1-ysize):
            for x in xrange(0,self.width-1-xsize):
                boardcut = self.board[y:y+ysize,x:x+xsize]
                boardcut2 = self.board[x:x+xsize,y:y+ysize]
                Print(boardcut)
                Print(boardcut2)
                if self.compare(boardcut, pattern):
                    x,y = self.findX(pattern)


    def turn(self): # play your turn and add it to your internal data structure
        self.find_pattern(PLAYER,OPONENT,[[32,33,34],[42,43,44]])
        if P.terminateAI:
            return
        # if self.isFree(x,y):
            # break
        return 0,0

        # if i > 1:
        #     P.pipeOut("DEBUG {} coordinates didn't hit an empty field".format(i))
        # pass
        #  C:\Python27\Scripts\pyinstaller.exe main.py pipe.py ai1.py --name pbrain-sim.exe --onefile