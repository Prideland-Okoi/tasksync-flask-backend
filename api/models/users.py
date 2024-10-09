# auth.py
from api import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    verification_code = db.Column(db.String(6), nullable=True)
    verification_sent_at = db.Column(db.DateTime, nullable=True)  # New field to track when the code was sent
    verified = db.Column(db.Boolean, default=False)
    resend_attempts = db.Column(db.Integer, default=0)  # Track number of resends
    last_resend_at = db.Column(db.DateTime, nullable=True)  # Track the last time a resend was requested


    def __repr__(self):
        return f"User('{self.username}')"

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'email': self.email,
            'verified': self.verified
        }

