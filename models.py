# models.py
import flask_sqlalchemy
from app import db


class Groceries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(120))
    
    def __init__(self, i):
        self.item = i
        
    def __repr__(self):
        return '<Grocery Item: %s>' % self.item 

