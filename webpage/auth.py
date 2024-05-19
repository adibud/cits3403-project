from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

# Create a Blueprint named 'auth' for authentication-related routes
auth = Blueprint('auth', __name__)

# Define the LoginForm using FlaskForm
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Define the RegistrationForm using FlaskForm
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

# Route for logging in users
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            # If user exists and password is correct, log them in
            login_user(user, remember=True)
            return redirect(url_for('main.dashboard'))
        else:
            # Flash an error message if login fails
            flash('Login unsuccessful. Please check email and password.', category='error')
    # Render the login template with the form
    return render_template('login.html', form=form)

# Route for registering new users
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter((User.email == form.email.data) | (User.username == form.username.data)).first()
        if existing_user:
            # Check if email or username already exists
            if existing_user.email == form.email.data:
                flash('Email address already exists', category='error')
            else:
                flash('Username already exists', category='error')
        else:
            # Hash the password and create a new user
            hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
            new_user = User(email=form.email.data, username=form.username.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            # Log the user in after registration
            login_user(new_user)
            return redirect(url_for('main.dashboard'))
    # Render the registration template with the form
    return render_template('register.html', form=form)

# Route for logging out users
@auth.route('/logout')
@login_required  # Ensure only logged-in users can access this route
def logout():
    # Log out the current user
    logout_user()
    return redirect(url_for('main.index'))
   
