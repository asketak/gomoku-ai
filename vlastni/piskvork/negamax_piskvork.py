from __future__ import print_function
import random
import math
from pprint import pprint
from pipe import DEBUG_EVAL, DEBUG
import sys
import pipe as pp
import numpy as np
from decimal import *
from ai_negamax import GomokuGame
from easyAI import TwoPlayersGame, Human_Player, AI_Player, Negamax, DUAL,SSS

class ai():
    def __init__(self):  # empty init, not insert anything
        return None

    def init(self, width):  # called at start of game
        self.start = True
        self.width = width
        self.ai_algo = DUAL(2)
        self.ttt = GomokuGame([Human_Player(), AI_Player(self.ai_algo)],width,2)


    def my(self, x, y):  # add your turn to internal data structure
        self.ttt.play_move([x,y])

    def opp(self, x, y):  # add opponent turn to internal data structure
        if self.start:
            self.ttt = GomokuGame([Human_Player(), AI_Player(self.ai_algo)],self.width,1)
            self.start = False

        self.ttt.play_move([x,y])

    def turn(self):  # play your turn and add it to your internal data structure
        self.start = False
        ai_move = self.ttt.get_move()
        # print(ai_move)
        return ai_move[0],ai_move[1]

        # if i > 1:
        #     pp.pipeOut("DEBUG {} coordinates didn't hit an empty field".format(i))
        # pass
        #  C:\Python27\Scripts\pyinstaller.exe main.py pipe.py ai_negamax.py --name pbrain-sim.exe --onefile

#pyinstaller negamax_piskvork.py main.py pipe.py --name pbrain-tod.exe --onefile
