# app.py
from os.path import join, dirname
from dotenv import load_dotenv
import os
import flask
import flask_sqlalchemy
import flask_socketio
import models

CHAT_HISTORY_BROADCAST_CHANNEL = 'Chat history received'

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

def emit_chat_history(channel):
    chat_history = [ \
        (db_message.sender + ": " + db_message.message) for db_message \
        in db.session.query(models.ChatHistory_DB).all()]
    chat_history.reverse() # Want newest message first
        
    socketio.emit(channel, {
        'chatHistory': chat_history
    })


@socketio.on('connect')
def on_connect():
    print('Someone connected!')
    global anonNum
    defaultuser = 'Anonymous{}'.format(anonNum)
    socketio.emit('connected', {
        'defaultUsername': defaultuser
    })
    anonNum += 1
    print("Assigned new user this username: {}".format(defaultuser))
    emit_chat_history(CHAT_HISTORY_BROADCAST_CHANNEL)
    

@socketio.on('disconnect')
def on_disconnect():
    print ('Someone disconnected!')

@socketio.on('new message')
def on_new_message(data):
    print("Got an event for adding this message to the chat history:\n\t{}: {}".format(data["sender"], data["msg"]))

    db.session.add(models.ChatHistory_DB(data["sender"], data["msg"]));
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
        host=os.getenv('IP', '127.0.0.1'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )
