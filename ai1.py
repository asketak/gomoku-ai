from __future__ import print_function
import random
import pipe as pp
from pipe import DEBUG_EVAL, DEBUG
import sys

# play randomly 

class ai():
    def __init__(self): # empty init, not insert anything
    	return None

    def isFree(self,x, y): # check if x/y cell is free
        return x >= 0 and y >= 0 and x < self.width and y < self.height and self.board[x][y] == 0

    def init(self,width,height): # called at start of game
        self.width = width
        self.height = height

        self.board = [[0 for i in xrange(width)] for j in xrange(height)]

    def my(self,x,y): # add your turn to internal data structure
        self.board[x][y] = 1

    def opp(self,x,y): #add opponent turn to itnernal data structure
        self.board[x][y] = 2

    def turn(self): # play your turn and add it to your internal data structure
        i = 0
        while True:
            x = random.randint(0, self.width-1)
            y = random.randint(0, self.height-1)
            i += 1
            print(str(x) + ":" + str(y), file = sys.stderr)
            if pp.terminateAI:
                return
            if self.isFree(x,y):
                break
        return x,y

        # if i > 1:
        #     pp.pipeOut("DEBUG {} coordinates didn't hit an empty field".format(i))
        # pass
        #  C:\Python27\Scripts\pyinstaller.exe main.py pipe.py ai1.py --name pbrain-sim.exe --onefile