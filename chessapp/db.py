
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
            password=os.getenv('DBPASSWORD'),
            cursor_factory=psycopg2.extras.DictCursor)

    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM information_schema.tables WHERE table_name=%s", ('users',))
        if cursor.fetchone()[0]:
            return True
        cursor.execute(open('chessapp/schema.sql', 'r').read())
        for i in range(10):
            cursor.execute(
                '''INSERT INTO chessboard
                   DEFAULT VALUES'''
            )
            cursor.execute(
                '''INSERT INTO practice_board
                   DEFAULT VALUES'''
            )
        db.commit()git
        return False
    
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables"""
    tableAlreadyPresent = init_db()
    if tableAlreadyPresent:
        click.echo('Database already present.')
    else:
        click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

