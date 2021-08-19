from chessapp import create_app
from flask_socketio import SocketIO, emit
import config

app = create_app()
socketio = SocketIO(app)

@socketio.on('my event')
def handle_my_custom_event(json):
     
     emit('my response', json)


if __name__=="__main__":
    socketio.run(app, debug=True, host=str(config.Config.SERVER))