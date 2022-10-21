from ..extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    messages = db.relationship('Message', backref='message')

    def __repr__(self):
        return '<User {}>'.format(self.username)
