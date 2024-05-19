from . import db
from flask_login import UserMixin
from datetime import datetime

# Define the User model, extending UserMixin for Flask-Login integration
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each user
    username = db.Column(db.String(150), unique=True, nullable=False)  # Username (must be unique)
    email = db.Column(db.String(150), unique=True, nullable=False)  # Email (must be unique)
    password = db.Column(db.String(150), nullable=False)  # Password (hashed)
    points = db.Column(db.Integer, default=0)  # Points awarded to the user
    bio = db.Column(db.String(300), nullable=True)  # Optional bio field for the user
    profile_picture = db.Column(db.String(150), nullable=True)  # Optional profile picture field
    requests = db.relationship('Request', backref='user', lazy=True)  # Relationship to requests created by the user
    comments = db.relationship('Comment', backref='author', lazy=True)  # Relationship to comments made by the user
    badges = db.relationship('Badge', backref='user', lazy=True)  # Relationship to badges earned by the user

# Define the Request model
class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each request
    title = db.Column(db.String(150), nullable=False)  # Title of the request
    descr = db.Column(db.String(500), nullable=False)  # Description of the request
    image = db.Column(db.String(150), nullable=True)  # Optional image for the request
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key linking to the user who created the request
    comments = db.relationship('Comment', backref='request', lazy=True)  # Relationship to comments on the request

# Define the Comment model
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each comment
    text = db.Column(db.String(200), nullable=False)  # Text of the comment
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)  # Date the comment was created
    commenter_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key linking to the user who made the comment
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'), nullable=False)  # Foreign key linking to the request being commented on

# Define the Badge model
class Badge(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each badge
    name = db.Column(db.String(150), nullable=False)  # Name of the badge
    description = db.Column(db.String(300), nullable=True)  # Optional description of the badge
    icon = db.Column(db.String(150), nullable=True)  # Optional icon for the badge
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Foreign key linking to the user who earned the badge
