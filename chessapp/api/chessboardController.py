from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

import config
from __main__ import api
from chessapp import dbAlchemy
from chessapp.models import ChessboardModel, HistoryModel


class Chessboard(Resource):
    def get(self, board_id):
        board = ChessboardModel.query.filter_by(id=board_id).first()
        if not board:
            abort(404, message=f'Board id:{board_id} not found')
        # user = ChessboardModel.query.filter_by(id=board_id).first()
        return board.serialize()


api.add_resource(Chessboard, "/api/chessboard/<int:board_id>")



