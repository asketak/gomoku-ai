from easyAI import Human_Player, AI_Player, Negamax
from easyAI import TwoPlayersGame, Human_Player, AI_Player,  DUAL
from negamax import Negamax
from pprint import pprint
from flask import Flask, render_template_string, request, make_response
from ai_negamax_faster import GomokuGame
from easyAI import TT

ai = Negamax(7, tt = TT())
game = GomokuGame( [ AI_Player(ai), Human_Player() ],15,1)
import cProfile
cProfile.run("game.play(1)") 