from flask import Blueprint, request
from flask_socketio import emit, join_room, leave_room
from app import socketio
from app import message_service
from app import error_messages
from app import ClientSchema
from marshmallow import ValidationError


socket = Blueprint('socket', __name__)

# I'm going to keep the clients inside a dictionary because I can access each client in O(1) time
clients = {}


@socketio.on('join_room')
def handle_join_room(data):
    sid = request.sid
    room = data['roomName']

    # Map client data
    client = {
        'sid': sid,
        'username': data['username'],
        'room_name': data['roomName']
    }

    # Loop through all clients and check if the username is already taken for a room
    for client in clients.values():
        if client['username'] == data['username'] and client['room_name'] == data['roomName']:
            response = {'joined': False, 'errors': error_messages.USERNAME_TAKEN_FOR_ROOM}
            emit('join_room', response, to=sid)
            return

    try:
        # Validate client data
        client_schema = ClientSchema()
        client = client_schema.load(client)

        # Add client to clients dictionary
        clients[sid] = client

        # Join client to room
        join_room(room)

        response = {'joined': True}
        emit('join_room', response, to=room)
    except ValidationError as err:
        response = {'joined': False, 'errors': err.messages}

        emit('join_room', response, to=sid)


@socketio.on('leave_room')
def handle_leave_room(data):
    room = data['roomName']
    username = data['username']
    leave_room(room)

    # remove client from clients list
    try:
        del clients[request.sid]
    except KeyError:
        pass

    response_to_client = {'left': True}
    response_to_room = {'leaver': username}

    emit('receive_message', response_to_room, to=room)
    emit('leave_room', response_to_client)
    return


@socketio.on('send_message')
def send_message(data):
    sid = request.sid
    room = data['roomName']

    # Each time a message is sent, save it to the database
    added_message, is_valid = message_service.add_message(data)

    if not is_valid:
        emit('send_message', {'error': error_messages.MESSAGE_NOT_ADDED}, to=sid)
        return

    emit('receive_message', data, to=room)
