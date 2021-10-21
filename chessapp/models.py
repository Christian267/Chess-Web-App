from flask_sqlalchemy import SQLAlchemy

from __main__ import dbAlchemy


class ChessboardModel(dbAlchemy.Model):
    __tablename__ = 'chessboard'
    id = dbAlchemy.Column(dbAlchemy.Integer, primary_key=True)
    white_id = dbAlchemy.Column(dbAlchemy.Integer)
    black_id = dbAlchemy.Column(dbAlchemy.Integer)
    fen = dbAlchemy.Column(dbAlchemy.String(100))

    def __repr__(self):
        return f"Chessboard(white_id = {white_id}, black_id = {black_id}, fen = {fen})"

    def serialize(self):
        return {
            'id': self.id,
            'white_id': self.white_id,
            'black_id': self.black_id,
            'fen': self.fen
        }


class ChessboardModel(dbAlchemy.Model):
    __tablename__ = 'practice_board'
    id = dbAlchemy.Column(dbAlchemy.Integer, primary_key=True)
    fen = dbAlchemy.Column(dbAlchemy.String(100))

    def __repr__(self):
        return f"Practice Board(fen = {fen})"

    def serialize(self):
        return {
            'id': self.id,
            'fen': self.fen
        }

class HistoryModel(dbAlchemy.Model):
    __tablename__ = 'history'
    id = dbAlchemy.Column(dbAlchemy.Integer, primary_key=True)
    time_played = dbAlchemy.Column(dbAlchemy.DateTime(timezone=True), default=dbAlchemy.func.now())
    winner_id = dbAlchemy.Column(dbAlchemy.Integer, dbAlchemy.ForeignKey('users.id'))
    loser_id = dbAlchemy.Column(dbAlchemy.Integer, dbAlchemy.ForeignKey('users.id'))
    elo_change = dbAlchemy.Column(dbAlchemy.Integer, nullable=False)

    def __repr__(self):
        return f"History Match(winner_id = {winner_id}, loser_id = {loser_id}, elo_change = {elo_change})"

    def serialize(self):
        return {
            'id': self.id,
            'time_played': self.time_played,
            'winner_id': self.winner_id,
            'loser_id': self.loser_id,
            'elo_change': self.elo_change
        }
        

class UserModel(dbAlchemy.Model):
    __tablename__ = 'users'
    id = dbAlchemy.Column(dbAlchemy.Integer, primary_key=True)
    username = dbAlchemy.Column(dbAlchemy.String(100), nullable=False)
    elo = dbAlchemy.Column(dbAlchemy.Integer, nullable=False)

    def __repr__(self):
        return f"User(username = {username}, view = {views}, likes = {likes})"

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'elo': self.elo
        }