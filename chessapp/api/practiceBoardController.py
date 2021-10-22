from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

import config
from __main__ import api
from chessapp import dbAlchemy
from chessapp.models import PracticeboardModel, HistoryModel


user_put_args = reqparse.RequestParser()
user_put_args.add_argument("fen", type=str, help="FEN is required", required=True)


class Practiceboard(Resource):
    def get(self, board_id):
        board = PracticeboardModel.query.filter_by(id=board_id).first()
        if not board:
            abort(404, message=f'Board id:{board_id} not found')
        return board.serialize()

    def put(self, board_id):
        board = PracticeboardModel.query.filter_by(id=board_id).first()
        if not board:
            abort(404, message=f'Board id:{board_id} not found')
        args = user_put_args.parse_args()
        board.fen = args['fen']
        dbAlchemy.session.commit()
        return board.serialize()


api.add_resource(Practiceboard, "/api/practiceboard/<int:board_id>")



