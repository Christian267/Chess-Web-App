
from chessapp import create_app
from chessapp.db import get_db

from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy, declarative_base
from flask_restful import Api, Resource

import config

app = create_app()
socketio = SocketIO(app)
api = Api(app)
db_sa= SQLAlchemy(app)

Base = declarative_base()

from chessapp.sockets import chessEvents
from chessapp.api import userController

if __name__=='__main__':
    socketio.run(app, debug=True, host=str(config.DevelopmentConfig.SERVER))