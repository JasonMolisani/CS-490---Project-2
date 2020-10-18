# app.py
from os.path import join, dirname
from dotenv import load_dotenv
import os
import flask
import flask_sqlalchemy
import flask_socketio
import models
import bot

CHAT_HISTORY_BROADCAST_CHANNEL = 'Chat history received'
MAX_MESSAGE_LENGTH = 480
MESSAGE_LENGTH_ERROR_MESSAGE = "Incoming message was too long and wasn't saved. Please limit messages to {} characters".format(MAX_MESSAGE_LENGTH)
MAX_DISPLAYED_MESSAGES = 32
BOT_NAME = 'DadBot'

app = flask.Flask(__name__)

socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

dotenv_path = join(dirname(__file__), 'project2.env')
load_dotenv(dotenv_path)

database_uri = os.environ['DATABASE_URL']

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)
db.init_app(app)
db.app = app


db.create_all()
db.session.commit()

anonNum = 0
numUsers = 0

chatBot = bot.Bot(name=BOT_NAME)

def emit_chat_history(channel):
    # The list conprehension will be used once the database gets redesigned, but until then the patchy for loop will do
    chat_history = [ \
        {'senderPic': db_message.sender.picUrl, 'message': db_message.message, 'class': db_message.senderClass} for db_message \
        in db.session.query(models.chatHistory).all()]
        
    socketio.emit(channel, {
        'chatHistory': chat_history[-min(len(chat_history), MAX_DISPLAYED_MESSAGES):]
    })


@socketio.on('connect')
def on_connect():
    print('Someone connected!')
    
    # Generate a default username for the new connection
    global anonNum
    defaultuser = 'Anonymous{}'.format(anonNum)
    anonNum += 1
    print("Assigned new user this username: {}".format(defaultuser))
    
    # Update the number of users currently connected
    global numUsers
    numUsers += 1
    
    # Transmit the default username, number of users, and chat history
    socketio.emit('someone connected', {
        'defaultUsername': defaultuser,
        'numUsers': numUsers
    })
    emit_chat_history(CHAT_HISTORY_BROADCAST_CHANNEL)
    

@socketio.on('disconnect')
def on_disconnect():
    print ('someone disconnected!')
    
    # Update the number of users currently connected and broadcast that change
    global numUsers
    numUsers -= 1
    socketio.emit('someone disconnected', {
        'numUsers': numUsers
    })
    

@socketio.on('new message')
def on_new_message(data):
    print("Got an event for adding this message to the chat history:\n\t{}: {}".format(data["sender"], data["msg"]))

    if len(models.registeredUsers.query.filterby(id=data["sender"]).all):
        # If the sender id is not in the database, don't add the message
        print("Message not added due to invalid sender ID")
        return
    elif len(data["msg"]) > MAX_MESSAGE_LENGTH:
        db.session.add(models.chatHistory(chatBot.name, MESSAGE_LENGTH_ERROR_MESSAGE, "bot"));
    else:
        db.session.add(models.chatHistory(data["sender"], data["msg"], "user"));
    db.session.commit();
    
    emit_chat_history(CHAT_HISTORY_BROADCAST_CHANNEL)
    
    if len(data['msg']) >= 2 and data['msg'][0:2]=="!!":
        botReply = chatBot.parseCommand(data['msg'][2:])
        
        db.session.add(models.chatHistory(botReply["sender"], botReply["msg"], "bot"));
        db.session.commit();
        
        emit_chat_history(CHAT_HISTORY_BROADCAST_CHANNEL)

@app.route('/')
def index():
    models.db.create_all()
    anonNum = 0
    emit_chat_history(CHAT_HISTORY_BROADCAST_CHANNEL)
    
    return flask.render_template("index.html")

if __name__ == '__main__': 
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )
