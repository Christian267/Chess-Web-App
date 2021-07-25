import os
from flask import Flask

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
    
    # Register routes
    app.register_blueprint(view, url_prefix='/')
    
    return app
