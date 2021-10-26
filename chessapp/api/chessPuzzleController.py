from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

import config
from __main__ import api
from chessapp import dbAlchemy
from chessapp.models import ChessPuzzleModel
from chessapp.api.chessPuzzleService import validate_fen


user_post_args = reqparse.RequestParser()
user_post_args.add_argument('fen', type=str, help='Fen is required', required=True)
user_post_args.add_argument('solution', type=str, help='Solution is required', required=True)


class ChessPuzzle(Resource):
    def post(self):
        args = user_post_args.parse_args()
        res = validate_fen(args['fen'])
        if not res['isValid']:
            abort(400, message='Invalid fen', 
                       error_count=res['error_count'],
                       error_messages=res['error_messages'])
        queryResult = ChessPuzzleModel.query.filter_by(fen=args['fen']).first()
        if queryResult:
            abort(409, message=f'This puzzle has already been submitted')
        print(args['solution'])
        newPuzzle = ChessPuzzleModel(fen=args['fen'], solution=args['solution'])
        dbAlchemy.session.add(newPuzzle)
        dbAlchemy.session.commit()
        return newPuzzle.serialize()
    
    def get(self):
        result = ChessPuzzleModel.query.all()
        puzzles = {}
        for i in range(len(result)):
            puzzles[result[i].id] = {
                                      'fen': result[i].fen,
                                      'solution': result[i].solution
                                    }
        return puzzles





api.add_resource(ChessPuzzle, "/api/chesspuzzle/")