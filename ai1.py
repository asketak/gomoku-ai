import random
import pipe as pp
from pipe import DEBUG_EVAL, DEBUG

board,weight_board = None, None

def isFree(x, y):
	return x >= 0 and y >= 0 and x < pp.width and y < pp.height and board[x][y] == 0

def init():
	board = [[0 for i in xrange(pp.width)] for j in xrange(pp.height)]
	weight_board = [[0 for i in xrange(pp.width)] for j in xrange(pp.height)]

def my():
	board[x][y] = 1

def opp():
	board[x][y] = 2

def turn():
	i = 0
	while True:
		x = random.randint(0, pp.width)
		y = random.randint(0, pp.height)
		i += 1
		if pp.terminateAI:
			return
		if isFree(x,y):
			break
	board[x][y] = 1
	return x,y

	# if i > 1:
	# 	pp.pipeOut("DEBUG {} coordinates didn't hit an empty field".format(i))
	# pass