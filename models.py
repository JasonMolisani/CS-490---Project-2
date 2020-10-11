# models.py
import flask_sqlalchemy
from app import db


class ChatHistory_DB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(120))
    message = db.Column(db.String(120))
    
    def __init__(self, usr, msg):
        self.sender = usr
        self.message = msg
        
    def __repr__(self):
        return '<{}: {}>'.format(self.sender, self.message)

