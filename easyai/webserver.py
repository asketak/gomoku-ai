from easyAI import TwoPlayersGame, Human_Player, AI_Player, Negamax, DUAL
from pprint import pprint
from flask import Flask, render_template_string, request, make_response
from ai_negamax_faster import GomokuGame
import codecs
import pickle
from easyAI import TT
import numpy as np

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
ai_algo = DUAL(2,  win_score= 1000000)
width = 15

def pack(arr):
  ret = {}
  for x in xrange(0,width):
    for y in xrange(0,width):
      if arr[x][y] != 0:
        ret[(x,y)] = arr[x][y]
  return ret
  
def unpack(dict):
  arr = np.zeros((width, width), np.int8)
  for x,y in dict:
    arr[x][y] = dict[(x,y)] 

  arr = tuple(map(tuple, arr))
  return arr

@app.route("/", methods=['GET', 'POST'])
def play_game():
    global ttt 
    game_cookie = request.cookies.get('game_board')
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
    pickled = (pickle.dumps(pack(ttt.hboard)))
    resp.set_cookie("game_board", pickled)
    if reset:
        ttt = GomokuGame([Human_Player(), AI_Player(ai_algo)],width,1)
        ttt.hboard = tuple(np.zeros((width, width), np.int8))
        ttt.htob()
        resp.set_cookie('game_board', '', expires=0)
    return resp


if __name__ == "__main__":
    global ttt 
    ttt = GomokuGame([Human_Player(), AI_Player(ai_algo)],width,1)
    app.run()


 