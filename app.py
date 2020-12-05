# app.py
from os.path import join, dirname
from dotenv import load_dotenv
import os
import flask
import flask_sqlalchemy
import flask_socketio
import bot
from flask import request

CHAT_HISTORY_BROADCAST_CHANNEL = "Chat history received"
MAX_MESSAGE_LENGTH = 480
MESSAGE_LENGTH_ERROR_MESSAGE = "Incoming message was too long and wasn't saved. Please limit messages to {} characters".format(
    MAX_MESSAGE_LENGTH
)
MAX_DISPLAYED_MESSAGES = 14
BOT_EMAIL = "DadBot@fakeEmail.com"
BOT_PIC = "/static/origami_dragon.jpg"

app = flask.Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

dotenv_path = join(dirname(__file__), "project2.env")
load_dotenv(dotenv_path)

database_uri = os.environ["DATABASE_URL"]

app.config["SQLALCHEMY_DATABASE_URI"] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)
import models

db.init_app(app)
db.app = app


# db.create_all()
# db.session.commit()

anonNum = 0
numUsers = 0

chatBot = bot.Bot()
loggedInUsers = set()


def emit_chat_history(channel):
    # The list conprehension will be used once the database gets redesigned, but until then the patchy for loop will do
    chat_history = [
        {
            "senderPic": db_message.sender.picUrl,
            "message": db_message.message,
            "class": db_message.senderClass,
        }
        for db_message in db.session.query(models.chatHistory).all()
    ]

    for sid in loggedInUsers:
        socketio.emit(
            channel,
            {
                "chatHistory": chat_history[
                    -min(len(chat_history), MAX_DISPLAYED_MESSAGES) :
                ]
            },
            room=sid,
        )


@socketio.on("connect")
def on_connect():
    print("Someone connected!")

    # Update the number of users currently connected
    global numUsers

    # Transmit the default username, number of users, and chat history
    socketio.emit("someone connected", {"numUsers": numUsers})


@socketio.on("disconnect")
def on_disconnect():
    print("someone disconnected!")

    global loggedInUsers
    if request.sid in loggedInUsers:
        loggedInUsers.remove(request.sid)

    # Update the number of users currently connected and broadcast that change
    global numUsers
    numUsers = len(loggedInUsers)
    socketio.emit("someone disconnected", {"numUsers": numUsers})


@socketio.on("new user login")
def accept_login(data):
    email = data["email"]
    profilePic = data["picUrl"]
    print("received login request for email: {}".format(email))

    # If this is a new user, add it to the database
    if (len(models.registeredUsers.query.filter_by(email=email, picUrl=profilePic).all()) == 0):
        db.session.add(models.registeredUsers(email, profilePic))
        db.session.commit()
        print("New user registered to the database")
    else:
        print("User was already registered")

    senderDBkey = (
        models.registeredUsers.query.filter_by(email=email, picUrl=profilePic)
        .first()
        .id
    )

    global loggedInUsers
    loggedInUsers.add(request.sid)

    socketio.emit(
        "login accepted",
        {
            "email": email,
            "picUrl": profilePic,
            "senderKey": senderDBkey,
        },
        room=request.sid,
    )

    global numUsers
    numUsers = len(loggedInUsers)

    socketio.emit("someone logged in", {"numUsers": numUsers})

    emit_chat_history(CHAT_HISTORY_BROADCAST_CHANNEL)


@socketio.on("new message")
def on_new_message(data):
    print(
        "Got an event for adding this message to the chat history:\n\t{}: {}".format(
            data["sender"], data["msg"]
        )
    )

    treatedMsg = chatBot.adjustMessageHTML(data["msg"])
    if len(models.registeredUsers.query.filter_by(id=data["sender"]).all()) == 0:
        # If the sender id is not in the database, don't add the message
        print("Message not added due to invalid sender ID")
        return
    elif len(treatedMsg) > MAX_MESSAGE_LENGTH:
        db.session.add(
            models.chatHistory(chatBot.DB_Id, MESSAGE_LENGTH_ERROR_MESSAGE, "bot")
        )
    else:
        db.session.add(models.chatHistory(data["sender"], treatedMsg, "user"))
    db.session.commit()

    emit_chat_history(CHAT_HISTORY_BROADCAST_CHANNEL)

    if len(data["msg"]) >= 2 and data["msg"][0:2] == "!!":
        botReply = chatBot.parseCommand(data["msg"][2:])

        db.session.add(models.chatHistory(botReply["sender"], botReply["msg"], "bot"))
        db.session.commit()

        emit_chat_history(CHAT_HISTORY_BROADCAST_CHANNEL)


@app.route("/")
def index():
    models.db.create_all()
    global anonNum
    anonNum = 0
    emit_chat_history(CHAT_HISTORY_BROADCAST_CHANNEL)

    return flask.render_template("index.html")


def login_bot(botEmail, botPicUrl):
    if (
        len(
            models.registeredUsers.query.filter_by(
                email=botEmail, picUrl=botPicUrl
            ).all()
        )
        == 0
    ):
        db.session.add(models.registeredUsers(botEmail, botPicUrl))
        db.session.commit()
    chatBot.DB_Id = (
        models.registeredUsers.query.filter_by(email=botEmail, picUrl=botPicUrl)
        .first()
        .id
    )


if __name__ == "__main__":
    login_bot(BOT_EMAIL, BOT_PIC)
    socketio.run(
        app,
        host=os.getenv("IP", "127.0.0.1"),
        port=int(os.getenv("PORT", 5432))
    )
