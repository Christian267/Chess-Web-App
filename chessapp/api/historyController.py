from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

import config
from __main__ import api, db_sa, Base
from chessapp.db import get_db

class HistoryModel(db_sa.Model):
    __tablename__ = 'history'
    id = db_sa.Column(db_sa.Integer, primary_key=True)
    time_played = db_sa.Column(db_sa.DateTime(timezone=True), default=func.now())
    winner_id = db_sa.Column(db_sa.Integer, db.ForeignKey('users.id'))
    loser_id = db_sa.Column(db_sa.Integer, db.ForeignKey('users.id'))
    elo_change = db_sa.Column(db_sa.Integer, nullable=False)

    def __repr__(self):
        return f"User(username = {username}, view = {views}, likes = {likes})"

    def serialize(self):
        return {
            'id': self.id,
            'time_played': self.time_played,
            'winner_id': self.winner_id,
            'loser_id': self.loser_id,
            'elo_change': self.elo_change
        }