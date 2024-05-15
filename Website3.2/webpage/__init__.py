from flask import Flask, render_template, render_template, request, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()




# Create a Flask app
def create_app(): 
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_database.db'
    db.init_app(app)

    # Define a route and its associated function
    @app.route('/')
    def hello_world():
        return render_template('home2.html')
    
    from .auth import auth
    from .main import main

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(main, url_prefix='/')

    from .models import users

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return users.query.get(int(id))

    with app.app_context():
        db.create_all()
    
    return app


 


  