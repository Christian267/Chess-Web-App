
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

import config
from __main__ import api, db_sa, Base
from chessapp.db import get_db

class UserModel(db_sa.Model):
    __tablename__ = 'users'
    id = db_sa.Column(db_sa.Integer, primary_key=True)
    username = db_sa.Column(db_sa.String(100), nullable=False)
    elo = db_sa.Column(db_sa.Integer, nullable=False)

    def __repr__(self):
        return f"User(username = {username}, view = {views}, likes = {likes})"

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'elo': self.elo
        }

user_put_args = reqparse.RequestParser()
user_put_args.add_argument("elo", type=int, help="User elo required", required=True)

user_update_args = reqparse.RequestParser()
user_update_args.add_argument("username", type=str, help="Username is required")
user_update_args.add_argument("elo", type=int, help="New elo required")

class User(Resource):
    def get(self, user_username):
        print(user_username)
        result = UserModel.query.filter_by(username=user_username).first()
        if not result:
            abort(404, message=f'User {user_username} not found')
        user = UserModel.query.filter_by(username=user_username).first()
        return user.serialize()

    def put(self, user_username):
        args = user_put_args.parse_args()
        result = UserModel.query.filter_by(username=user_username).first()
        if result:
            abort(409, message=f'Username {user_username} already taken')
        user = UserModel(username=user_username, elo=args['elo'])
        db_sa.session.add(user)
        db_sa.session.commit()
        return user.serialize(), 201

    def patch(self, user_username):
        args = user_update_args.parse_args()
        result = UserModel.query.filter_by(username=user_username).first()
        print(args)
        if not result:
            abort(404, message=f'User {user_username} not found, cannot update')
        if args['username']:
            result.username = args['username']
        if args['elo']:
            result.elo = args['elo']
        db_sa.session.commit()

        return result.serialize()

    def delete(self, user_username):
        result = UserModel.query.filter_by(username=user_username).first()
        if not result:
            abort(404, message=f"User {user_username} not found")
        user = UserModel.query.filter_by(username=user_username).first()
        db_sa.session.delete(user)
        db_sa.session.commit()
        return user.serialize()

api.add_resource(User, "/user/<string:user_username>")



