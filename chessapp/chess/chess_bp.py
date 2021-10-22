import functools

from flask import Blueprint
from flask import Blueprint, flash, g, redirect, render_template, request,\
                  session, url_for, jsonify
                  
from chessapp.db import get_db
from chessapp import dbAlchemy
from chessapp.models import ChessboardModel, PracticeboardModel

chess_bp = Blueprint('chess_bp', __name__,
            template_folder='templates',
            static_folder='static')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash('Login before entering a chess match', category='error')  
            return redirect(url_for('auth.login'))

        return view(**kwargs)
    return wrapped_view

@chess_bp.route('/roomselect')
def roomselect():
    chessboardRows = ChessboardModel.query.all()
    practiceBoardRows = PracticeboardModel.query.all()
    for i in range(len(chessboardRows)):
        if chessboardRows[i].fen == 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1':
            chessboardRows[i].status = 'Available'
        else:
            chessboardRows[i].status = 'Game In Progress'
        if practiceBoardRows[i].fen == 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1':
            practiceBoardRows[i].status = 'Available'
        else:
            chessboardRows[i].status = 'In Use'
        dbAlchemy.session.commit()
        chessboardRows[i] = chessboardRows[i].serialize()
        practiceBoardRows[i] = practiceBoardRows[i].serialize()
    chessboardRows.sort(key=lambda chessboardRow: chessboardRow['id'])
    practiceBoardRows.sort(key=lambda practiceBoardRow: practiceBoardRow['id'])
    return render_template('chess/roomselect.html', **{'chessboards': chessboardRows, 'practiceboards': practiceBoardRows})

@chess_bp.route('/chessboard', methods=['GET'])
@login_required
def chessboard():
    room = request.args.to_dict()
    return render_template('chess/chessboard.html', room=room)

@chess_bp.route('/practiceboard', methods=['GET'])
@login_required
def practiceboard():
    room = request.args.to_dict()
    return render_template('chess/practiceboard.html', room=room)

@chess_bp.route('/get_username')
def get_username():
    data = {'username': ''}
    if g.user:
        data['username'] = g.user['username']
    return jsonify(data)

@chess_bp.route('/get_players')
def get_players():
    db = get_db()
    with db.cursor() as cursor:
        players = cursor.execute(
        '''SELECT white AND black 
            FROM   chessboard 
            WHERE  id = 1'''
        )
    return players

@chess_bp.route('/get_fen')
def get_fen():
    roomType = request.json('roomType')
    roomNumber = request.json('roomNumber')
    if roomType == 'chessboard':
        board = ChessboardModel.query.filter_by(id=roomNumber).first()
    else:
        board = PracticeboardModel.query.filter_by(id=roomNumber).first()
    data = {'fen': board.fen}
    # db = get_db()
    # data = {'board_position': ''}
    # with db.cursor() as cursor:
    #     cursor.execute(
    #         '''SELECT fen
    #         FROM   chessboard
    #         WHERE  id = 1'''
    #     )
    #     board_position = cursor.fetchone()['fen']
    # data['board_position'] = board_position
    return jsonify(data)

@chess_bp.route('/resetboard')
def resetboard():
    db = get_db()
    chess_starting_position_fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    with db.cursor() as cursor:
        cursor.execute(
        '''UPDATE chessboard 
            SET    fen = %s 
            WHERE  id = 1''', 
            (chess_starting_position_fen,)
        )
    db.commit()
    return redirect(url_for('views.home'))

