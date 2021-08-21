
from chessapp import create_app
from chessapp.db import get_db
from flask_socketio import SocketIO, emit
import config

app = create_app()
socketio = SocketIO(app)

@socketio.on('connect')
def handle_connection():
     emit('connect', broadcast=True, include_self=False)

@socketio.on('set color')
def handle_set_color(playerColor):
     """
     :param playerColor: dict
     """
     # playerColor = json.loads(color)
     dbColor = playerColor['color']
     db = get_db()
     db.execute(
          f'UPDATE chessboard SET {dbColor} = ? WHERE id = 1', (playerColor['name'],)
     )
     db.commit()
     whitePlayer = db.execute(
          'SELECT white FROM chessboard'
     ).fetchone()['white']
     blackPlayer = db.execute(
          'SELECT black FROM chessboard'
     ).fetchone()['black']

     players = {'white': whitePlayer, 'black': blackPlayer}
     emit('set player colors', players, broadcast=True)

@socketio.on('chess move')
def handle_chess_move(move):
     emit('chess move', move, broadcast=True, include_self=False)

@socketio.on('game end')
def handle_game_end(results):
     db = get_db()
     if results['winner'] != 'Empty' and results['loser'] != 'Empty' and results['winner'] != results['loser']:
          winnerElo = db.execute(
               'SELECT elo FROM user WHERE username = ?', (results['winner'],)
          ).fetchone()['elo']
          loserElo = db.execute(
               'SELECT elo FROM user WHERE username = ?', (results['loser'],)
          ).fetchone()['elo']
          winnerElo, loserElo = calculateEloChange(winnerElo, loserElo)
          db.execute(
               'UPDATE user SET elo = ? WHERE username = ?', (winnerElo, results['winner'])
          )
          db.execute(
               'UPDATE user SET elo = ? WHERE username = ?', (loserElo, results['loser'])
          )

     db.execute(
          'INSERT INTO history (winner, loser) VALUES (?,?)', (results['winner'], results['loser'])
     )
     db.execute(
          'UPDATE chessboard SET white = ? WHERE id = 1', ('Empty',)
     )
     db.execute(
          'UPDATE chessboard SET black = ? WHERE id = 1', ('Empty',)
     )
     db.commit()

def calculateEloChange(winnerElo, loserElo):
     expectedWinner = 1 / (1 + 10 ** ((loserElo - winnerElo)/400))
     expectedLoser = 1 - expectedWinner
     winnerElo = round(winnerElo + 50 * (1 - expectedWinner))
     loserElo = round(loserElo - 50 * (expectedLoser))
     return winnerElo, loserElo


if __name__=='__main__':
    socketio.run(app, debug=True, host=str(config.Config.SERVER))