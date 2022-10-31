from flask_socketio import SocketIO
from flask import Flask
from config import Config
from .extensions import db, migrate

# Model import
from .models.message import Message

# Schema import
from .schemas.message_schema import MessageSchema
from .schemas.client_schema import ClientSchema

# Service import
from .services import message_service

# Constants import
from .constants import error_messages

socketio = SocketIO()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from .resources.socket import socket
    app.register_blueprint(socket)

    socketio.init_app(app, cors_allowed_origins=app.config['ALLOWED_ORIGINS'])
    return app
