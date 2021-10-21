import functools

from flask import Blueprint
from flask import Blueprint, flash, g, redirect, render_template, request,\
                  session, url_for, jsonify
                  
from chessapp.db import get_db

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
    return render_template('chess/roomselect.html')

@chess_bp.route('/chessboard_room/<int:room>')
def chessboard_room(room):
    return redirect(url_for('chess_bp.chessboard', room=room))

@chess_bp.route('/chessboard', methods=['GET'])
@login_required
def chessboard():
    db = get_db()
    room = request.args.to_dict()
    print(room)
    return render_template('chess/chessboard.html')

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
            WHERE  id = 0'''
        )
    return players

@chess_bp.route('/get_fen')
def get_fen():
    db = get_db()
    data = {'board_position': ''}
    with db.cursor() as cursor:
        cursor.execute(
            '''SELECT fen
            FROM   chessboard
            WHERE  id = 1'''
        )
        board_position = cursor.fetchone()['fen']
    data['board_position'] = board_position
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

