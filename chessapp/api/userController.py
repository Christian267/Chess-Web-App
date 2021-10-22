from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import config
from __main__ import api
from chessapp import dbAlchemy
from chessapp.models import UserModel


user_put_args = reqparse.RequestParser()
user_put_args.add_argument("elo", type=int, help="User elo required", required=True)
user_put_args.add_argument("pw", type=str, help="Password required", required=True)

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
        hashedPassword = generate_password_hash(args['pw'], method='sha256')
        user = UserModel(username=user_username, pw=hashedPassword, elo=args['elo'])
        dbAlchemy.session.add(user)
        dbAlchemy.session.commit()
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
        dbAlchemy.session.commit()

        return result.serialize()

    def delete(self, user_username):
        result = UserModel.query.filter_by(username=user_username).first()
        if not result:
            abort(404, message=f"User {user_username} not found")
        user = UserModel.query.filter_by(username=user_username).first()
        dbAlchemy.session.delete(user)
        dbAlchemy.session.commit()
        return user.serialize()

api.add_resource(User, "/user/<string:user_username>")



