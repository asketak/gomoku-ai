from easyAI import TwoPlayersGame, Human_Player, AI_Player, Negamax
from pprint import pprint
from flask import Flask, render_template_string, request, make_response
from ai_negamax import GomokuGame
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
            <button type="submit" name="choice" value="{{i}} {{j}}"
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
ai_algo = Negamax(3, tt=TT())
width = 10


@app.route("/", methods=['GET', 'POST'])
def play_game():
    # ttt = GomokuGame([Human_Player(), AI_Player(ai_algo)],width)
    game_cookie = request.cookies.get('game_board')
    reset = False
    if game_cookie:
        # ttt.hboard = [int(x) for x in game_cookie.split(",")]
        ttt.hboard = pickle.loads(codecs.decode(game_cookie.encode(), "base64"))
        ttt.htob()
    if "choice" in request.form:
        coord = [ map(int, x) for x in request.form["choice"].split()]
        ttt.play_move(coord)
        pprint(coord)
        if not ttt.is_over():
            ai_move = ttt.get_move()
            ttt.play_move(ai_move)
    if "reset" in request.form:
        ttt.hboard = tuple(np.zeros((width, width), np.int8))
        ttt.htob()
        reset = True

    if ttt.is_over():
        msg = ttt.winner()
    else:
        msg = "play move"
    resp = make_response(render_template_string(TEXT, ttt=ttt, msg=msg))
    pickled = codecs.encode(pickle.dumps(ttt.hboard), "base64").decode()
    resp.set_cookie("game_board", pickled)
    if reset:
        resp.set_cookie('game_board', '', expires=0)
    return resp


if __name__ == "__main__":
    global ttt 
    ttt = GomokuGame([Human_Player(), AI_Player(ai_algo)],width)
    app.run()