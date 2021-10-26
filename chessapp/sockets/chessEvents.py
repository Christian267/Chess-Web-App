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
     socketRooms = rooms()
     room = ''
     for r in socketRooms:
          if r.startswith('chessboard') or r.startswith('practice_board'):
               room = r
     roomWords = room.split()
     roomType = roomWords[0]
     roomNumber = roomWords[1]
     leave_room(room)
     decrement_user_count(roomType, roomNumber)
     # emit('leave room announcement', data, room=room, include_self=False)
     emit('disconnect')

@socketio.on('join room')
def handle_join_room(data):
     roomType = data['roomType']
     roomNumber = data['roomNumber']
     room = roomType + ' ' + roomNumber
     username = data['username']
     join_room(room)
     increment_user_count(roomType, roomNumber)
     print('User', username, 'has joined', room)
     emit('join room announcement', data, room=room, include_self=False)

# @socketio.on('leave room')
# def handle_leave_room(data):
#      room = data['room']


@socketio.on('set color')
def handle_set_color(data):
     """
     Handles updating the player color tag on the chessboard page.
     :param data: dict{'roomType': str, 'roomNumber': int, 'color': str, 'username': str}
     """
     roomType = data['roomType']
     roomNumber = data['roomNumber']
     room = roomType + ' ' + roomNumber
     if 'color' in data:
          update_player_color(data['color'], data['username'], roomType, roomNumber)
     white_player = get_player('white', roomType, roomNumber)
     black_player = get_player('black', roomType, roomNumber)
     players = {'white': white_player, 'black': black_player}
     emit('set player colors', players, room=room)

@socketio.on('chess move')
def handle_chess_move(data):
     roomType = data['roomType']
     roomNumber = data['roomNumber']
     room = roomType + ' ' + roomNumber
     update_board_state(data['board_state'], roomType, roomNumber)
     emit('chess move', data['move'], room=room, include_self=False)

@socketio.on('game end')
def handle_game_end(data):
     """
     Once a chess game concludes, this method updates user elo, adds the match the match history table,
     and resets the players on the board
     :param data: dict{'winner': str, 'loser': str}
     """
     print('GAME END, data:', data)
     roomType = data['roomType']
     roomNumber = data['roomNumber']
     winner = data['winner']
     loser = data['loser']
     if winner != 'Empty' and loser != 'Empty' and winner != loser:
          winner_id = get_user_id(winner)
          loser_id = get_user_id(loser)
          winner_elo = get_elo(winner_id)
          loser_elo = get_elo(loser_id)
          game_length = get_game_length(roomType, roomNumber)
          winner_elo, loser_elo, elo_change = calculate_elo_change(winner_elo, loser_elo)
          add_game_to_history(winner_id, loser_id, elo_change, game_length)
          update_elo(winner_id,  winner_elo)
          update_elo(loser_id, loser_elo)
     reset_chessboard(roomType, roomNumber)
     

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
             (winner_id, loser_id, elo_change, int(game_length))
          )     
     db.commit()

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

def decrement_user_count(roomType, roomNumber):
     if roomType == 'chessboard':
          board = ChessboardModel.query.filter_by(id=int(roomNumber)).first()
     else:
          board = PracticeboardModel.query.filter_by(id=int(roomNumber)).first()
     board.user_count -= 1
     if board.user_count < 0:
          board.user_count = 0
     dbAlchemy.session.commit()

     

def increment_user_count(roomType, roomNumber):
     if roomType == 'chessboard':
          board = ChessboardModel.query.filter_by(id=int(roomNumber)).first()
     else:
          board = PracticeboardModel.query.filter_by(id=int(roomNumber)).first()
     board.user_count += 1
     dbAlchemy.session.commit()

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

def get_game_length(roomType, roomNumber):
     board = ChessboardModel.query.filter_by(id=roomNumber).first()
     return board.turn_number

def get_player(color, roomType, roomNumber):
     """
     Values used to update the player tags on the chessboard UI.
     """
     if roomType == 'chessboard':
          board = ChessboardModel.query.filter_by(id=int(roomNumber)).first()
     else:
          board = PracticeboardModel.query.filter_by(id=int(roomNumber)).first()

     if color == 'white':
          return board.white
     return board.black

     # db = get_db()
     # with db.cursor() as cursor:
     #      cursor.execute(
     #           f'''SELECT {color} 
     #               FROM   chessboard
     #               WHERE id=1'''
     #      )
     #      return cursor.fetchone()[color]

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

def update_board_state(board_state, roomType, roomNumber):
     """
     Updates the board state to a new fen. Called every time a player makes a
     move on the chessboard.
     """
     if roomType == 'chessboard':
          board = ChessboardModel.query.filter_by(id=int(roomNumber)).first()
          board.turn_number += 1
     else:
          board = PracticeboardModel.query.filter_by(id=int(roomNumber)).first()
     board.fen = board_state
     dbAlchemy.session.commit()


     # db = get_db()
     # with db.cursor() as cursor:
     #      cursor.execute(
     #           '''UPDATE chessboard
     #              SET    fen = %s
     #              WHERE  id = 1''',
     #              (board_state,)
     #      )
     # db.commit()

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

def update_player_color(player_color, player_name, roomType, roomNumber):
     """
     Updates the player color in the chessboard table. This value corresponds to the 
     player color on the chessboard page UI.
     """
     if roomType == 'chessboard':
          board = ChessboardModel.query.filter_by(id=int(roomNumber)).first()
     else:
          board = PracticeboardModel.query.filter_by(id=int(roomNumber)).first()

     if player_color == 'white':
          board.white = player_name
     else:
          board.black = player_name
     dbAlchemy.session.commit()

     # if player_color is None or player_name is None:
     #      return
     # db = get_db()
     # with db.cursor() as cursor:
     #      cursor.execute(
     #           f'''UPDATE chessboard
     #               SET    {player_color} = %s
     #               WHERE id = 1''',
     #               (player_name,)
     #      )
     # db.commit()

def reset_chessboard(roomType, roomNumber):
     """
     Reverts the board back to its starting position, ready to start a new game.
     """
     db = get_db()
     chess_starting_fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
     with db.cursor() as cursor:
          cursor.execute(
          '''UPDATE chessboard 
             SET    white = %s, black = %s, fen = %s, turn_number = 0
             WHERE  id = %s''', 
             ('Empty', 'Empty', chess_starting_fen, int(roomNumber))
          )
          # cursor.execute(
          # '''UPDATE chessboard 
          #    SET    black = %s 
          #    WHERE  id = %s''', 
          #    ('Empty', roomNumber)
          # )     
          # cursor.execute(
          # '''UPDATE chessboard 
          #    SET    fen = %s 
          #    WHERE  id = %s''', 
          #    (chess_starting_fen, roomNumber)
          # )
     db.commit()


