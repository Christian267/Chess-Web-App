import functools

from flask import Blueprint
from flask import Blueprint, flash, g, redirect, render_template, request,\
                  session, url_for, jsonify
                  
from chessapp.db import get_db

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password1']
        passwordConfirm = request.form['password2']
        print(username, password, passwordConfirm)
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
                return redirect(url_for('auth.login'))
        flash(error)
    return render_template('register.html')

@auth.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username, password)
        db = get_db()
        error = None
        with db.cursor() as cursor:
            cursor.execute(
            '''SELECT  * 
                FROM   users 
                WHERE  username = %s''',
                (username,))
            if not username:
                error = 'Username is required.'
            user_id = None
            # cursor.fetchone() is transient, returns None after 1st call
            cursor_fetch = cursor.fetchone() 
            if cursor_fetch is not None:
                user_id = cursor_fetch['id']
            elif not error:
                error = 'Could not find username'
            if error is None:
                session.clear()
                session['user_id'] = user_id
                return redirect(url_for('views.home'))

        flash(error)
    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('views.home'))

