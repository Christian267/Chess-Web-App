
import psycopg2, psycopg2.extras
import click
from flask import current_app, g
from flask.cli import with_appcontext
import os

def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(
            host=os.getenv('DBHOST'),
            database=os.getenv('DBNAME'),
            user=os.getenv('DBUSER'),
            cursor_factory=psycopg2.extras.DictCursor)

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(open('chessapp/schema.sql', 'r').read())
        chess_starting_position_fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
        cursor.execute(
        '''INSERT INTO chessboard (white, black, fen) 
            VALUES (%s, %s, %s)''', 
            ('Empty', 'Empty', chess_starting_position_fen)
        )
        db.commit()
    
@click.command('init-db')
@with_appcontext
def init_db_command():
    """CLear the existing data and create new tables"""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

