from flask_socketio import emit, join_room, leave_room, rooms

from chessapp.db import get_db
from chessapp import dbAlchemy 
from chessapp.models import ChessboardModel, UserModel, PracticeboardModel

try:
    from __main__ import socketio
except:
    from socketservice import socketio

@socketio.on('connect')
def handle_connection():
     emit('connect', include_self=False)

@socketio.on('disconnect')
def handle_disconnect():
     roomss = rooms()
     room = ''
     for r in roomss:
          if r.startswith('Competitive Lobby') or r.startswith('Practice Lobby'):
               room = r
     leave_room(room)
     decrement_user_count(room)
     # emit('leave room announcement', data, room=room, include_self=False)
     emit('disconnect')

@socketio.on('join room')
def handle_join_room(data):
     room = data['room']
     username = data['username']
     join_room(room)
     increment_user_count(room)
     print('User', username, 'has joined', room)
     emit('join room announcement', data, room=room, include_self=False)

@socketio.on('leave room')
def handle_leave_room(data):
     room = data['room']


@socketio.on('set color')
def handle_set_color(playerColor):
     """
     Handles updating the player color tag on the chessboard page.
     :param playerColor: dict{'color': str, 'name': str}
     """
     if playerColor:
          update_player_color(playerColor['color'], playerColor['name'])
     white_player = get_player('white')
     black_player = get_player('black')
     players = {'white': white_player, 'black': black_player}
     emit('set player colors', players, broadcast=True)

@socketio.on('chess move')
def handle_chess_move(json):
     update_board_state(json['board_state'])
     emit('chess move', json['move'], broadcast=True, include_self=False)

@socketio.on('game end')
def handle_game_end(results):
     """
     Once a chess game concludes, this method updates user elo, adds the match the match history table,
     and resets the players on the board
     :param results: dict{'winner': str, 'loser': str}
     """
     winner = results['winner']
     loser = results['loser']
     if winner != 'Empty' and loser != 'Empty' and winner != loser:
          winner_id = get_user_id(winner)
          loser_id = get_user_id(loser)
          winner_elo = get_elo(winner_id)
          loser_elo = get_elo(loser_id)
          winner_elo, loser_elo, elo_change = calculate_elo_change(winner_elo, loser_elo)
          add_game_to_history(winner_id, loser_id, elo_change, game_length)
          update_elo(winner_id,  winner_elo)
          update_elo(loser_id, loser_elo)
     reset_chessboard()
     

# Utilities
def add_game_to_history(winner_id, loser_id, elo_change, game_length):
     """
     Called at the end of a valid chess game. Records winner and loser in addition to
     the elo rating change that occurred as a result.
     """
     db = get_db()
     with db.cursor() as cursor:
          cursor.execute(
          '''INSERT INTO history (winner_id, loser_id, elo_change, game_length) 
             VALUES (%s, %s, %s, %s)''', 
             (winner_id, loser_id, elo_change, game_length)
          )     
     db.commit()

def get_elo(user_id):
     db = get_db()
     with db.cursor() as cursor:
          cursor.execute(
               '''SELECT elo 
                  FROM   users 
                  WHERE  id = %s''', 
                  (user_id,)
               )
          return cursor.fetchone()['elo']

def calculate_elo_change(winner_elo, loser_elo):
     """
     Once a match is over, calculate and return elo changes to update the database.
     :param winner_elo: int
     :param loser_elo: int
     :return winner_elo: int
     :return loser_elo: int
     :return elo_change: int
     """
     odds_of_winning = 1 / (1 + 10 ** ((loser_elo - winner_elo)/400))
     elo_change = round(50 * (1 - odds_of_winning))
     winner_elo = winner_elo + elo_change
     loser_elo = loser_elo - elo_change
     return winner_elo, loser_elo, elo_change

def decrement_user_count(room):
     roomType = room[:-2]
     roomNumber = room[-1]
     print('DECREMENT_USER_COUNT, roomType:', roomType, 'roomNumber:', roomNumber)
     if roomType == 'Competitive Lobby':
          board = ChessboardModel.query.filter_by(id=int(roomNumber)).first()
     else:
          board = PracticeboardModel.query.filter_by(id=int(roomNumber)).first()
     board.user_count -= 1
     if board.user_count < 0:
          board.user_count = 0
     print('Decrementing user count:', board.user_count + 1, '->', board.user_count)
     dbAlchemy.session.commit()

     

def increment_user_count(room):
     roomType = room[:-2]
     roomNumber = room[-1]
     print('INCREMENT_USER_COUNT, roomType:', roomType, 'roomNumber:', roomNumber)
     if roomType == 'Competitive Lobby':
          board = ChessboardModel.query.filter_by(id=int(roomNumber)).first()
     else:
          board = PracticeboardModel.query.filter_by(id=int(roomNumber)).first()
     board.user_count += 1
     print('Incrementing user count:', board.user_count - 1, '->', board.user_count)
     dbAlchemy.session.commit()

def get_player(color):
     """
     Values used to update the player tags on the chessboard UI.
     """
     db = get_db()
     with db.cursor() as cursor:
          cursor.execute(
               f'''SELECT {color} 
                   FROM   chessboard
                   WHERE id=1'''
          )
          return cursor.fetchone()[color]

def get_user_id(username):
     """
     
     """
     db = get_db()
     with db.cursor() as cursor:
          cursor.execute(
          '''SELECT id
             FROM   users
             WHERE username = %s''',
             (username,)
          )
          return cursor.fetchone()['id']

def update_board_state(board_state):
     """
     Updates the board state to a new fen. Called every time a player makes a
     move on the chessboard.
     """
     db = get_db()
     with db.cursor() as cursor:
          cursor.execute(
               '''UPDATE chessboard
                  SET    fen = %s
                  WHERE  id = 1''',
                  (board_state,)
          )
     db.commit()

def update_elo(user_id, elo):
     """
     Called after the end of a valid chess game. Commits update to elo into
     the users table of the database.
     """
     db = get_db()
     with db.cursor() as cursor:
          cursor.execute(
          '''UPDATE users 
             SET    elo = %s 
             WHERE  id = %s''', 
             (elo, user_id)
          )
     db.commit()

def update_player_color(player_color=None, player_name=None):
     """
     Updates the player color in the chessboard table. This value corresponds to the 
     player color on the chessboard page UI.
     """
     if player_color is None or player_name is None:
          return
     db = get_db()
     with db.cursor() as cursor:
          cursor.execute(
               f'''UPDATE chessboard
                   SET    {player_color} = %s
                   WHERE id = 1''',
                   (player_name,)
          )
     db.commit()

def reset_chessboard():
     """
     Reverts the board back to its starting position, ready to start a new game.
     """
     db = get_db()
     chess_starting_position_fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
     with db.cursor() as cursor:
          cursor.execute(
          '''UPDATE chessboard 
             SET    white = %s 
             WHERE  id = 1''', 
             ('Empty',)
          )
          cursor.execute(
          '''UPDATE chessboard 
             SET    black = %s 
             WHERE  id = 1''', 
             ('Empty',)
          )     
          cursor.execute(
          '''UPDATE chessboard 
             SET    fen = %s 
             WHERE  id = 1''', 
             (chess_starting_position_fen,)
          )
     db.commit()


