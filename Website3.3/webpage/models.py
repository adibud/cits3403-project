from . import db 
from flask_login import UserMixin 
from sqlalchemy import func

class requests(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    descr = db.Column(db.String)
    quantity = db.Column(db.Integer)
    image = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    com = db.relationship('comments', backref='requests', lazy=True)

class users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(200), unique=True)
    req = db.relationship('requests', backref='users', lazy=True)

class comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    time_created = db.Column(db.DateTime, default=func.now(), nullable=False)
    request_id = db.Column(db.Integer, db.ForeignKey('requests.id'), nullable=False)
    commenter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    commenter = db.relationship('users', backref='comments')
