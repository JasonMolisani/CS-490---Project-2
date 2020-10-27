'''Defines the databases and their relationships used for the app'''
from app import db


class registeredUsers(db.Model):
    '''Database to track the registeredUsers who have ever logged in to the chat room'''
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64))
    picUrl = db.Column(db.String(128))
    loggedIn = db.Column(db.Boolean)
    messages = db.relationship("chatHistory", backref="sender")

    def __init__(self, usrEmail, usrPicUrl):
        self.email = usrEmail
        self.picUrl = usrPicUrl


class chatHistory(db.Model):
    '''Database to track the messages sent in the chat room. Message sender will refer to a registered user tuple in the preceeding database'''
    id = db.Column(db.Integer, primary_key=True)
    senderDBkey = db.Column(
        db.Integer, db.ForeignKey(registeredUsers.id), nullable=False
    )
    message = db.Column(db.String(480))
    senderClass = db.Column(db.String(16))

    def __init__(self, sendKey, msg, clss):
        self.senderDBkey = sendKey
        self.message = msg
        self.senderClass = clss
