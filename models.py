# models.py
import flask_sqlalchemy
from app import db


class chatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    senderDBkey = db.Column(db.Integer)
    message = db.Column(db.String(480))
    senderClass = db.Column(db.String(16))
    
    def __init__(self, sendKey, msg, clss):
        self.senderDBkey = sendKey
        self.message = msg
        self.senderClass = clss
        
    def __repr__(self):
        return '{}: {}'.format(self.sender, self.message)
