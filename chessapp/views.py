import functools
from flask import Blueprint
from flask import Blueprint, flash, g, redirect, render_template, request,\
                  session, url_for
from chessapp.db import get_db

view = Blueprint('views', __name__)


@view.route('/')
def home():
    return render_template('index.html')

@view.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = f'User {username} is already registered.'

        if error is None:
            db.execute(
                'INSERT INTO user (username) VALUES (?)', (username,)
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
            'SELECT * FROM user WHERE username = ?', (username,)
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
        if g.user is None:
            return redirect(url_for('views.login'))

        return view(**kwargs)

    return wrapped_view

@view.route('/chessboard')
@login_required
def chessboard():
    db = get_db()
    return render_template('chessboard.html')

@view.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

