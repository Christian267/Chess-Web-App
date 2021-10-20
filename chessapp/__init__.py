import os
from flask import Flask
from . import db

def create_app():
    """Construct the application"""

    # create and configure app
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Register context processor
    with app.app_context():
        from .views import view
        from .auth.auth import auth
        from .chess.chess_bp import chess_bp

    db.init_app(app)
    app.register_blueprint(view)
    app.register_blueprint(auth)
    app.register_blueprint(chess_bp)
    
    return app
