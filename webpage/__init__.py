from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Initialize SQLAlchemy for database interactions
db = SQLAlchemy()
# Initialize Flask-Migrate for handling database migrations
migrate = Migrate()

def create_app():
    # Create an instance of the Flask application
    app = Flask(__name__)
    
    # Set a secret key for secure session management
    app.config['SECRET_KEY'] = 'your secret key'
    
    # Configure the SQLite database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    # Bind SQLAlchemy and Migrate instances to the Flask app
    db.init_app(app)
    migrate.init_app(app, db)

    # Setup the LoginManager for handling user authentication
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # Specify the login view
    login_manager.init_app(app)

    # Import models to ensure they are registered with SQLAlchemy
    from .models import User, Request, Comment, Badge

    # Define the user loader callback for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        # Retrieve the user by their ID
        return User.query.get(int(user_id))

    # Register the authentication blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # Register the main blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
