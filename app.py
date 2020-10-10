# app.py
from os.path import join, dirname
from dotenv import load_dotenv
import os
import flask
import flask_sqlalchemy
import flask_socketio
import models 
import editdistance

GROCERY_BROADCAST_CHANNEL = 'Grocery list received'

app = flask.Flask(__name__)

socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

dotenv_path = join(dirname(__file__), 'project2.env')
load_dotenv(dotenv_path)

#sql_user = os.environ['SQL_USER']
#sql_pwd = os.environ['SQL_PASSWORD']
dbuser = os.environ['USER']

database_uri = os.environ['DATABASE_URL'] #'postgresql://{}:{}@localhost/postgres'.format(sql_user, sql_pwd)

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)
db.init_app(app)
db.app = app


db.create_all()
db.session.commit()

def emit_grocery_list(channel):
    grocery_list = [ \
        db_item.item for db_item \
        in db.session.query(models.Groceries).all()]
        
    socketio.emit(channel, {
        'groceryList': grocery_list
    })


@socketio.on('connect')
def on_connect():
    print('Someone connected!')
    socketio.emit('connected', {
        'test': 'Connected'
    })
    
    emit_grocery_list(GROCERY_BROADCAST_CHANNEL)
    

@socketio.on('disconnect')
def on_disconnect():
    print ('Someone disconnected!')

@socketio.on('new item input')
def on_new_address(data):
    print("Got an event for adding this item to the grocery list:", data)
    
    # Assume item is new, but check to see if that is really the case
    new_item = True
    for dbItem in db.session.query(models.Groceries).all():
        if editdistance.eval(data["item"], dbItem.item) <= 2:
            new_item = False
            break
    if new_item:
        db.session.add(models.Groceries(data["item"]));
        db.session.commit();
        
        emit_grocery_list(GROCERY_BROADCAST_CHANNEL)

@app.route('/')
def index():
    models.db.create_all()
    emit_grocery_list(GROCERY_BROADCAST_CHANNEL)

    return flask.render_template("index.html")

if __name__ == '__main__': 
    socketio.run(
        app,
        host=os.getenv('IP', '127.0.0.1'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )
