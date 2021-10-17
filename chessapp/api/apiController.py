
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort

from __main__ import api
from chessapp.db import get_db

user_put_args = reqparse.RequestParser()
user_put_args.add_argument("elo", type=int, help="User elo required", required=True)

users = {}

def abort_if_username_not_exist(username):
    if username not in users:
        abort(404, message="Username was not found.")

def abort_if_username_exists(username):
    if username in users:
        abort(409, message="Username already taken.")

class User(Resource):
    def get(self, username):
        abort_if_username_not_exist(username)
        return users[username]

    def put(self, username):
        abort_if_username_exists(username)
        args = user_put_args.parse_args()
        users[username] = args
        print(users)
        return users[username], 201

    def delete(self, username):
        abort_if_username_not_exist(username)
        del users[username]
        print(users)
        return '', 204

api.add_resource(User, "/user/<string:username>")



video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str)
video_put_args.add_argument("views", type=int)
video_put_args.add_argument("likes", type=int)

videos = {}

class Video(Resource):
    def get(self, video_id):
        return videos[video_id]

    def put(self, video_id):
        args = video_put_args.parse_args()
        return {video_id: args}

api.add_resource(Video, "/video/<int:video_id>")



