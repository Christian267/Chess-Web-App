from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from chessapp import create_app
import os
import sqlite3
import config
from flask_socketio import SocketIO, emit

app = create_app()
socketio = SocketIO(app)


if __name__=="__main__":
    socketio.run(app, debug=True, host=str(config.Config.SERVER))