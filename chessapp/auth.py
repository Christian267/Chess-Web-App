import functools

from flask import Blueprint
from flask import Blueprint, flash, g, redirect, render_template, request,\
                  session, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

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
                WHERE  lower(username) = %s''',
                (username.lower(),))
            # cursor.fetchone() is transient, returns None after 1st call
            cursor_fetch = cursor.fetchone()
            if not username:
                error = 'Username is required.'
            elif cursor_fetch is not None:
                error = f'Username {username} is already taken.'
            if password != passwordConfirm:
                error = 'Passwords don\'t match'
            if error is None:
                cursor.execute(
                '''INSERT INTO users (username, pass) 
                    VALUES (%s, %s)''', (username, generate_password_hash(password, method='sha256'))
                ) 
                db.commit()
                flash('Account created!', category='success')
                return redirect(url_for('auth.login'))
        flash(error, category='error')
    return render_template('register.html')

@auth.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
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
            if not password:
                error = 'Password is required'
            user_id = None
            # cursor.fetchone() is transient, returns None after 1st call
            cursor_fetch = cursor.fetchone() 
            if cursor_fetch:
                user_id = cursor_fetch['id']
                user_password = cursor_fetch['pass']
                print(user_id, user_password)
                if not check_password_hash(user_password, password):
                    error = 'Incorrect password'
            elif not error:
                error = 'Could not find username'
            if error is None:
                flash('Login Successful', category='success')
                session.clear()
                session['user_id'] = user_id
                return redirect(url_for('views.home'))

        flash(error, category='error')
    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('views.home'))

