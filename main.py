import sqlite3
import json
from chessapp import create_app
from chessapp.db import get_db
from flask_socketio import SocketIO, emit
import config
from flask import jsonify

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
          'SELECT white FROM chessboard WHERE id = 1'
     ).fetchone()['white']
     blackPlayer = db.execute(
          'SELECT black FROM chessboard WHERE id = 1'
     ).fetchone()['black']

     players = {'white': whitePlayer, 'black': blackPlayer}
     emit('set player colors', players, broadcast=True)

@socketio.on('chess move')
def handle_chess_move(move):
     emit('chess move', move, broadcast=True, include_self=False)

@socketio.on('game end')
def handle_game_end(results):
     db = get_db()
     db.execute(
          'INSERT INTO history (winner, loser) VALUES (SELECT id FROM user WHERE username = ?, SELECT id FROM user WHERE username = ?)', (results['winner'], results['loser'])
     )
     db.execute(
          'DELETE FROM chessboard WHERE id = 0'
     )
     db.execute(
        'INSERT INTO chessboard (white, black) VALUES (?, ?)', ('Empty', 'Empty')
     )
     db.commit()

if __name__=='__main__':
    socketio.run(app, debug=True, host=str(config.Config.SERVER))