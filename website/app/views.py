from flask import Flask, render_template, \
     redirect, request, session, flash, jsonify, url_for 

import io
import os
import uuid
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/chessboard')
def chessboard():
    return render_template('chessboard.html')

if __name__ == '__main__':
    app.run(debug=True)