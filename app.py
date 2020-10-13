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
MAX_MESSAGE_LENGTH = 120
MESSAGE_LENGTH_ERROR_MESSAGE = "Incoming message was too long and wasn't saved. Please limit messages to {} characters".format(MAX_MESSAGE_LENGTH)
MAX_DISPLAYED_MESSAGES = 24
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
    # chat_history = [ \
    #     {'sender': db_message.sender, 'message': db_message.message, 'class': 'user'} for db_message \
    #     in db.session.query(models.ChatHistory_DB).all()]
    chat_history = []
    for db_message in db.session.query(models.ChatHistory_DB).all():
        if db_message.sender == BOT_NAME:
            chat_history.append({'sender': db_message.sender, 'message': db_message.message, 'class': 'bot'})
        else:
            chat_history.append({'sender': db_message.sender, 'message': db_message.message, 'class': 'user'})
            
    chat_history.reverse() # Want newest message first
        
    socketio.emit(channel, {
        'chatHistory': chat_history[:min(len(chat_history), MAX_DISPLAYED_MESSAGES)]
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

    if len(data["msg"]) > MAX_MESSAGE_LENGTH:
        db.session.add(models.ChatHistory_DB(chatBot.name, MESSAGE_LENGTH_ERROR_MESSAGE));
    else:
        db.session.add(models.ChatHistory_DB(data["sender"], data["msg"]));
    db.session.commit();
    
    emit_chat_history(CHAT_HISTORY_BROADCAST_CHANNEL)
    
    if len(data['msg']) >= 2 and data['msg'][0:2]=="!!":
        botReply = chatBot.parseCommand(data['msg'][2:])
        
        db.session.add(models.ChatHistory_DB(botReply["sender"], botReply["msg"]));
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
