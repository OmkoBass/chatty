from flask import Blueprint
from flask_socketio import emit, join_room, leave_room
from .. import socketio

socket = Blueprint('socket', __name__)

@socketio.on('join_room')
def handle_join_room(data):
    room = data['roomName']
    join_room(room)

    response = { 'joined': True }

    emit('join_room', response, to=room)
    return

@socketio.on('leave_room')
def handle_leave_room(data):
    room = data['roomName']
    username = data['username']
    leave_room(room)

    response_to_client = { 'left': True }
    response_to_room = { 'leaver': username }

    emit('receive_message', response_to_room, to=room)
    emit('leave_room', response_to_client)
    return


@socketio.on('send_message')
def send_message(data):
    room = data['roomName']

    emit('receive_message', data, to=room)
