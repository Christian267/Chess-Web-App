from flask import Blueprint
from flask import Flask, render_template, \
     redirect, request, session, flash, jsonify, url_for 


view = Blueprint('views', __name__)


@view.route('/')
def home():
    return render_template('index.html')

@view.route('/login')
def login():
    return render_template('login.html')

@view.route('/chessboard')
def chessboard():
    return render_template('chessboard.html')
