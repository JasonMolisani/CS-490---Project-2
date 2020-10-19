# models.py
import flask_sqlalchemy
from app import db

class registeredUsers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64))
    picUrl = db.Column(db.String(128))
    loggedIn = db.Column(db.Boolean)
    messages = db.relationship('chatHistory', backref='sender')
    
    def __init__(self, usrEmail, usrPicUrl):
        self.email = usrEmail
        self.picUrl = usrPicUrl

class chatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    senderDBkey = db.Column(db.Integer, db.ForeignKey(registeredUsers.id), nullable=False)
    message = db.Column(db.String(480))
    senderClass = db.Column(db.String(16))
    
    def __init__(self, sendKey, msg, clss):
        self.senderDBkey = sendKey
        self.message = msg
        self.senderClass = clss
        
    def __repr__(self):
        return '{}: {}'.format(self.sender.email, self.message)
    