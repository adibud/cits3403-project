from . import db 
from flask_login import UserMixin 
from sqlalchemy import func, TIMESTAMP, text, ForeignKeyConstraint

class comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    request_id = db.Column(db.Integer, db.ForeignKey('requests.id'))




class requests(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    descr = db.Column(db.String)
    quantity = db.Column(db.Integer)
    image = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comm = db.relationship('comments', backref='requests', lazy=True)


class users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(200), unique=True)
    req = db.relationship('requests', backref='users', lazy=True)
    comm = db.relationship('comments', backref='users', lazy=True)    
   
