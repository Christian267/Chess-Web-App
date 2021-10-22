from flask_sqlalchemy import SQLAlchemy

from chessapp import dbAlchemy

class ChessboardModel(dbAlchemy.Model):
    __tablename__ = 'chessboard'
    id           = dbAlchemy.Column(dbAlchemy.Integer, primary_key=True)
    white        = dbAlchemy.Column(dbAlchemy.String(100), default='Empty', nullable=False)
    black        = dbAlchemy.Column(dbAlchemy.String(100), default='Empty', nullable=False)
    board_status = dbAlchemy.Column(dbAlchemy.String(100), default='Available', nullable=False)
    user_count   = dbAlchemy.Column(dbAlchemy.Integer,     default=0, nullable=False)
    fen          = dbAlchemy.Column(dbAlchemy.String(100), 
                default='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', 
                nullable=False)

    def __repr__(self):
        return f"Chessboard(white = {self.white}, black = {self.black}, board_status = {self.board_status}, user_count = {self.user_count}, fen = {self.fen})"

    def serialize(self):
        return {
            'id'            : self.id,
            'white'         : self.white,
            'black'         : self.black,
            'board_status'  : self.board_status,
            'user_count'    : self.user_count,
            'fen'           : self.fen
        }


class HistoryModel(dbAlchemy.Model):
    __tablename__ = 'history'
    id          = dbAlchemy.Column(dbAlchemy.Integer, primary_key=True)
    time_played = dbAlchemy.Column(dbAlchemy.DateTime(timezone=True), nullable=False, default=dbAlchemy.func.now())
    winner_id   = dbAlchemy.Column(dbAlchemy.Integer, dbAlchemy.ForeignKey('users.id'), nullable=False)
    loser_id    = dbAlchemy.Column(dbAlchemy.Integer, dbAlchemy.ForeignKey('users.id'), nullable=False)
    elo_change  = dbAlchemy.Column(dbAlchemy.Integer, nullable=False)
    game_length = dbAlchemy.Column(dbAlchemy.Integer, nullable=False)

    def __repr__(self):
        return f"History Match(winner_id = {self.winner_id}, loser_id = {self.loser_id}, elo_change = {self.elo_change}, game_length = {self.game_length})"

    def serialize(self):
        return {
            'id'         : self.id,
            'time_played': self.time_played,
            'winner_id'  : self.winner_id,
            'loser_id'   : self.loser_id,
            'elo_change' : self.elo_change,
            'game_length': self.game_length
        }
        

class PracticeboardModel(dbAlchemy.Model):
    __tablename__ = 'practice_board'
    id           = dbAlchemy.Column(dbAlchemy.Integer,     primary_key=True)
    board_status = dbAlchemy.Column(dbAlchemy.String(100), default='Available', nullable=False)
    user_count   = dbAlchemy.Column(dbAlchemy.Integer,     default=0, nullable=False)
    fen          = dbAlchemy.Column(dbAlchemy.String(100), 
        default='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
        nullable=False)

    def __repr__(self):
        return f"chessboard(board_status = {self.board_status}, user_count = {self.user_count} fen = {self.fen})"

    def serialize(self):
        return {
            'id'            : self.id,
            'board_status'  : self.board_status,
            'user_count'    : self.user_count,
            'fen'           : self.fen
        }

class UserModel(dbAlchemy.Model):
    __tablename__ = 'users'
    id       = dbAlchemy.Column(dbAlchemy.Integer,     primary_key=True)
    username = dbAlchemy.Column(dbAlchemy.String(100), nullable=False)
    pw       = dbAlchemy.Column(dbAlchemy.String(100), nullable=False)
    elo      = dbAlchemy.Column(dbAlchemy.Integer,     nullable=False)

    def __repr__(self):
        return f"User(username = {self.username}, elo = {self.elo})"

    def serialize(self):
        return {
            'id'        : self.id,
            'username'  : self.username,
            'pw'        : self.pw,
            'elo'       : self.elo
        }