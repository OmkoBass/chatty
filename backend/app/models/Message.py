from datetime import datetime
from app import db


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(128), nullable=False)
    username = db.Column(db.String(128), nullable=False)
    room_name = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Message {}>'.format(self.content)
