
from chessapp import create_app
from chessapp.db import get_db
from flask_socketio import SocketIO, emit
import config
import os

app = create_app()
socketio = SocketIO(app)
hasRun = False

@socketio.on('connect')
def handle_connection():
     emit('connect', broadcast=True, include_self=False)

@socketio.on('set color')
def handle_set_color(playerColor):
     """
     Handles updating the player color tag on the chessboard page and communicating to all clients.
     :param playerColor: dict
     """
     # playerColor = json.loads(color)
     if playerColor:
          db = get_db()
          dbColor = playerColor['color']
          db.execute(
               f'UPDATE chessboard SET {dbColor} = ? WHERE id = 1', (playerColor['name'],)
          )
          db.commit()
     whitePlayer = getPlayer('white')
     blackPlayer = getPlayer('black')

     players = {'white': whitePlayer, 'black': blackPlayer}
     emit('set player colors', players, broadcast=True)

@socketio.on('chess move')
def handle_chess_move(move):
     emit('chess move', move, broadcast=True, include_self=False)

@socketio.on('game end')
def handle_game_end(results):
     """
     Once a chess game concludes, this method updates user elo, adds the match the match history table,
     and resets the players on the board
     :param results: dict
     """
     db = get_db()
     winner = results['winner']
     loser = results['loser']
     if winner != 'Empty' and loser != 'Empty' and winner != loser:
          winnerElo = getElo(winner)
          loserElo = getElo(loser)
          eloChange = 0
          winnerElo, loserElo, eloChange = calculateEloChange(winnerElo, loserElo)
          addGameToHistory(winner, loser, winnerElo, loserElo, eloChange)
          updateElo(winner, winnerElo)
          updateElo(loser, loserElo)
     resetChessBoard()
     db.commit()

# Utilities
def getPlayer(color):
     db = get_db()
     return db.execute(
          f'SELECT {color} FROM chessboard'
     ).fetchone()[color]

def getElo(username):
     db = get_db()
     return db.execute(
               'SELECT elo FROM user WHERE username = ?', (username,)
          ).fetchone()['elo']

def updateElo(username, elo):
     db = get_db()
     db.execute(
          'UPDATE user SET elo = ? WHERE username = ?', (elo, username)
     )

def addGameToHistory(winner, loser, winnerElo, loserElo, eloChange):
     db = get_db()
     db.execute(
          'INSERT INTO history (winner, loser, winnerElo, loserElo, eloChange) VALUES (?, ?, ?, ?, ?)', (winner, loser, winnerElo, loserElo, eloChange)
     )     

def resetChessBoard():
     db = get_db()
     db.execute(
          'UPDATE chessboard SET white = ? WHERE id = 1', ('Empty',)
     )
     db.execute(
          'UPDATE chessboard SET black = ? WHERE id = 1', ('Empty',)
     )

def calculateEloChange(winnerElo, loserElo):
     """
     Once a match is over, calculate and return elo changes to update the database.
     :param winnerElo: int
     :param loserElo: int
     :return winnerElo: int
     :return loserElo: int
     :return eloChange: int
     """
     expectedWinner = 1 / (1 + 10 ** ((loserElo - winnerElo)/400))
     expectedLoser = 1 - expectedWinner
     eloChange = round(50 * (1 - expectedWinner))
     winnerElo = winnerElo + eloChange
     loserElo = loserElo - eloChange
     return winnerElo, loserElo, eloChange


if __name__=='__main__':
    socketio.run(app, debug=True, host=str(config.Config.SERVER))