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
    match_history = get_history(g.user['username'])
    print(match_history)
    return render_template('dashboard.html', **{'match_history': match_history})

@view.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif db.execute(
         '''SELECT id 
            FROM   user 
            WHERE  username = ?''', (username,)
        ).fetchone() is not None:
            error = f'User {username} is already registered.'

        if error is None:
            db.execute(
             '''INSERT INTO user (username) 
                VALUES (?)''', (username,)
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
        user = db.execute(
         '''SELECT * 
            FROM   user 
            WHERE  username = ?''', (username,)
        ).fetchone()

        if user is None:
            error = 'Could not find username.'
        
        if error is None:
            session.clear()
            session['user_id'] = user['id']
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
    players = db.execute(
     '''SELECT white AND black 
        FROM   chessboard 
        WHERE  id = 0'''
    )
    return players

@view.route('/get_fen')
def get_fen():
    db = get_db()
    data = {'board_position': ''}
    board_position = db.execute(
        '''SELECT fen
           FROM   chessboard
           WHERE  id = 1'''
    ).fetchone()['fen']
    data['board_position'] = board_position
    return jsonify(data)

@view.route('/get_history')
def get_history(username):
    db = get_db()
    userID = db.execute(
        '''SELECT id
           FROM user
           WHERE username = ?''',
           (username,)
    ).fetchone()['id']
    matchHistory = db.execute(
         '''SELECT winner.username     AS winner_username,
                   loser.username      AS loser_username,
                   winner.elo          AS winner_elo,
                   loser.elo           AS loser_elo,
                   history.elo_change  AS elo_change,
                   history.time_played AS time_played
            FROM history 
                INNER JOIN user AS winner
                    ON history.winner_id=winner.id
                INNER JOIN user AS loser
                    ON history.loser_id=loser.id
            WHERE winner.id=?
                OR loser.id=?
            ORDER BY time_played DESC''',
            (userID, userID)
    )
    return matchHistory

@view.route('/get_users')
def get_users():
    db = get_db()
    users = db.execute(
     '''SELECT * 
        FROM user 
        ORDER BY elo DESC'''
    )
    return users

@view.route('/resetboard')
def resetboard():
    db = get_db()
    chess_starting_position_fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    db.execute(
       '''UPDATE chessboard 
          SET    fen = ? 
          WHERE  id = 1''', 
          (chess_starting_position_fen,)
    )
    db.commit()
    return redirect(url_for('views.home'))

@view.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
         '''SELECT * 
            FROM   user 
            WHERE  id = ?''',
            (user_id,)
        ).fetchone()

