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
    return render_template('dashboard.html', **{'match_history': match_history})

@view.route('/leaderboard')
def leaderboard():
    users = get_users()
    return render_template('leaderboard.html', **{'users': users})

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
