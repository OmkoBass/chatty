from flask_socketio import SocketIO
from flask import Flask
from config import Config

socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from .resources.socket import socket
    app.register_blueprint(socket)

    socketio.init_app(app, cors_allowed_origins=app.config['ALLOWED_ORIGINS'])
    return app
