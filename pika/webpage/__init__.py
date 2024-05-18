from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_database.db'
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')  # Ensure this directory exists
    app.config['MAX_CONTENT_PATH'] = 1024 * 1024 * 10  # 10 MB limit for file uploads

    db.init_app(app)

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

    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    with app.app_context():
        db.create_all()

    return app
