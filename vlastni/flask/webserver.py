from easyAI import TwoPlayersGame, Human_Player, AI_Player,  DUAL
from negamax import Negamax
from pprint import pprint
from flask import Flask, render_template_string, request, make_response
from ai_negamax_faster import GomokuGame
import codecs
import pickle
from easyAI import TT
import numpy as np
import cProfile
import re

TEXT = '''
<!doctype html>
<html>
  <head><title>Gomoku game</title></head>
  <body>
    <h1>Gomoku game</h1>
    <h2>{{msg}}</h2>
    <form action="" method="POST">
      <table>
        {% for j in range(0, ttt.width ) %}
        <tr>
          {% for i in range(0, ttt.width) %}
          <td>
            <button type="submit" name="choice" value="{{i}},{{j}}"
             {{"disabled" if ttt.spot_string(j, i)!="_"}}>
              {{ttt.spot_string(j, i)}}
            </button>
          </td>
          {% endfor %}
        </tr>
        {% endfor %}
      </table>
      <button type="submit" name="reset">Start Over</button>
    </form>
  </body>
</html>
'''

app = Flask(__name__)
# ai_algo = Negamax(2 )
ai_algo = Negamax(3, tt = TT())
width = 15
@app.route("/", methods=['GET', 'POST'])
def play_game():
    global ttt 
    reset = False
    if "choice" in request.form:
        req = (request.form["choice"].split(','))
        coord = [ int(req[0]), int(req[1])]
        ttt.play_move(coord)
        if not ttt.is_over2():
            ai_move = ttt.get_move()
            ttt.play_move(ai_move)
    if "reset" in request.form:
        ttt.hboard = tuple(np.zeros((width, width), np.int8))
        ttt.htob()
        reset = True

    msg = ttt.winner()
    resp = make_response(render_template_string(TEXT, ttt=ttt, msg=msg))
    if reset:
        ttt = GomokuGame([Human_Player(), AI_Player(ai_algo)],width,1)
    return resp


if __name__ == "__main__":
    global ttt 
    ttt = GomokuGame([Human_Player(), AI_Player(ai_algo)],width,1)
    # cProfile.run('app.run()')
    app.run()


 