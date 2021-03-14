from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
import os
import sqlite3

app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('CHESS_WEBAPP_SETTING', silent=True)