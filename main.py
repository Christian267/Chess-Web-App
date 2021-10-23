
from chessapp import create_app
from chessapp.db import get_db

from flask_socketio import SocketIO, emit
from flask_restful import Api, Resource

import config

app = create_app()
socketio = SocketIO(app)
api = Api(app)


from chessapp.sockets import chessEvents
from chessapp.api import userController, chessboardController,\
    practiceBoardController, historyController, chessPuzzleController

if __name__=='__main__':
    socketio.run(app, debug=bool(config.DevelopmentConfig.DEBUG), host=str(config.DevelopmentConfig.SERVER))