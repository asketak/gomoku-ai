import random
import pipe as pp
from ai1 import ai as myai
from pipe import DEBUG_EVAL, DEBUG

pp.infotext = 'name="pbrain-sima", author="Tomas Sima", version="1.0", country="Czech Republic", www="https://github.com/stranskyjan/pbrain-pyrandom"'
ai = myai()
MAX_BOARD = 100
board = [[0 for i in xrange(MAX_BOARD)] for j in xrange(MAX_BOARD)]

def isFree(x, y):
    return x >= 0 and y >= 0 and x < pp.width and y < pp.height and board[x][y] == 0

def brain_init():
    if pp.width < 5 or pp.height < 5:
        pp.pipeOut("ERROR size of the board")
        return
    ai.init(pp.width, pp.height)
    pp.pipeOut("OK")

def brain_restart():
    ai.init(pp.width, pp.height)
    pp.pipeOut("OK")

def brain_my(x, y):
    ai.my(x,y)
    if isFree(x,y):
        board[x][y] = 1
    else:
        pp.pipeOut("ERROR my move [{},{}]".format(x, y))

def brain_opponents(x, y):
    if isFree(x,y):
        board[x][y] = 2
        ai.opp(x,y)
    else:
        pp.pipeOut("ERROR opponents's move [{},{}]".format(x, y))

def brain_block(x, y):
    pp.pipeOut("ERROR block not implemented")

def brain_takeback(x, y):
    return 1

def brain_turn():
    if pp.terminateAI:
        return

    x,y = ai.turn();
    pp.do_mymove(x, y)

    # i = 0
    # while True:
    #     x = random.randint(0, pp.width)
    #     y = random.randint(0, pp.height)
    #     i += 1
    #     if pp.terminateAI:
    #         return
    #     if isFree(x,y):
    #         break
    # if i > 1:
    #     pp.pipeOut("DEBUG {} coordinates didn't hit an empty field".format(i))

def brain_end():
    pass

def brain_about():
    pp.pipeOut(pp.infotext)

if DEBUG_EVAL:
    import win32gui
    def brain_eval(x, y):
        # TODO check if it works as expected
        wnd = win32gui.GetForegroundWindow()
        dc = win32gui.GetDC(wnd)
        rc = win32gui.GetClientRect(wnd)
        c = str(board[x][y])
        win32gui.ExtTextOut(dc, rc[2]-15, 3, 0, None, c, ())
        win32gui.ReleaseDC(wnd, dc)

# "overwrites" functions in pisqpipe module
pp.brain_init = brain_init
pp.brain_restart = brain_restart
pp.brain_my = brain_my
pp.brain_opponents = brain_opponents
pp.brain_block = brain_block
pp.brain_takeback = brain_takeback
pp.brain_turn = brain_turn
pp.brain_end = brain_end
pp.brain_about = brain_about
if DEBUG_EVAL:
    pp.brain_eval = brain_eval

def main():
    pp.main()

if __name__ == "__main__":
    main()