import functools
from flask import Blueprint
from flask import Blueprint, flash, g, redirect, render_template, request,\
                  session, url_for, jsonify
from chessapp.db import get_db

view = Blueprint('views', __name__)

@view.route('/')
def home():
    if g.user is None:
        return render_template('index.html')
    return redirect(url_for('views.dashboard'))

@view.route('/dashboard')
def dashboard():
    print(g.user['username'])
    match_history = get_history(g.user['username'])
    print(match_history)
    return render_template('dashboard.html', **{'match_history': match_history})

@view.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        db = get_db()
        error = None
        with db.cursor() as cursor:
            cursor.execute(
            '''SELECT  id 
                FROM   users 
                WHERE  username = %s''',
                (username,))
            if not username:
                error = 'Username is required.'
            elif cursor.fetchone() is not None:
                error = f'User {username} is already registered.'

            if error is None:
                cursor.execute(
                '''INSERT INTO users (username) 
                    VALUES (%s)''', (username,)
                ) 
                db.commit()
                return redirect(url_for('views.login'))
        flash(error)
    return render_template('register.html')

@view.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        db = get_db()
        error = None
        with db.cursor() as cursor:
            cursor.execute(
            '''SELECT  * 
                FROM   users 
                WHERE  username = %s''',
                (username,))
            user_id = cursor.fetchone()['id']
            if user_id is None:
                error = 'Could not find username.'
            
            if error is None:
                session.clear()
                session['user_id'] = user_id
                return redirect(url_for('views.home'))

        flash(error)
    return render_template('login.html')

@view.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('views.home'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        flash('Login before entering a chess match')  
        if g.user is None:
            return redirect(url_for('views.login'))

        return view(**kwargs)
    return wrapped_view

@view.route('/leaderboard')
def leaderboard():
    users = get_users()
    print(users)
    return render_template('leaderboard.html', **{'users': users})

@view.route('/chessboard')
@login_required
def chessboard():
    db = get_db()
    return render_template('chessboard.html')

@view.route('/get_username')
def get_username():
    data = {'username': ''}
    if g.user:
        data['username'] = g.user['username']
    return jsonify(data)

@view.route('/get_players')
def get_players():
    db = get_db()
    with db.cursor() as cursor:
        players = cursor.execute(
        '''SELECT white AND black 
            FROM   chessboard 
            WHERE  id = 0'''
        )
    return players

@view.route('/get_fen')
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

@view.route('/get_history')
def get_history(username):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(
            '''SELECT id
            FROM users
            WHERE username = %s''',
            (username,)
        )
        userID = cursor.fetchone()['id']
        cursor.execute(
            '''SELECT winner.username   AS winner_username,
                    loser.username       AS loser_username,
                    winner.elo           AS winner_elo,
                    loser.elo            AS loser_elo,
                    history.elo_change   AS elo_change,
                    history.time_played  AS time_played
                FROM   history 
                    INNER JOIN users AS winner
                        ON history.winner_id=winner.id
                    INNER JOIN users AS loser
                        ON history.loser_id=loser.id
                WHERE winner.id=%s
                    OR loser.id=%s
                ORDER BY time_played DESC''',
                (userID, userID)
        )
        matchHistory = cursor.fetchall()
    return matchHistory

@view.route('/get_users')
def get_users():
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(
        '''SELECT * 
            FROM users 
            ORDER BY elo DESC'''
        )
        users = cursor.fetchall()
    return users

@view.route('/resetboard')
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

@view.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    db = get_db()
    if user_id is None:
        g.user = None
    else:
        with db.cursor() as cursor:
            cursor.execute(
                '''SELECT * 
                    FROM   users 
                    WHERE  id = %s''',
                    (user_id,))
            g.user = cursor.fetchone()
