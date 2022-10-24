from flask_socketio import SocketIO
from flask import Flask
from config import Config
from .extensions import db, migrate

socketio = SocketIO()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.models import User, Message

    db.init_app(app)
    migrate.init_app(app, db)

    from .resources.socket import socket
    app.register_blueprint(socket)

    socketio.init_app(app, cors_allowed_origins=app.config['ALLOWED_ORIGINS'])
    return app
