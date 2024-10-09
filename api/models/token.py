# token.py
from api import db

class BlacklistedToken(db.Model):
    _tablename__ = 'blacklisted_tokens'

    token = db.Column(db.String(255), primary_key=True)

    def __repr__(self):
        return f'<BlacklistedToken {self.token}>'
