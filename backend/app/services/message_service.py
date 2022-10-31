from app import db
from app import Message
from app import MessageSchema
from marshmallow import ValidationError


def get_all_messages():
    schema = MessageSchema()

    return schema.dump(Message.query.all(), many=True)


def add_message(message):
    # Map content and room name to message
    message['content'] = message['message']
    message['room_name'] = message['roomName']
    try:
        schema = MessageSchema()

        # Validate message and map to Message model
        message = schema.dump(message)

        msg = Message(content=message['content'], username=message['username'], room_name=message['room_name'])

        db.session.add(msg)
        db.session.commit()

        # The second argument is wether the message is valid or not
        return msg, True
    except ValidationError as err:
        return err.messages, False
