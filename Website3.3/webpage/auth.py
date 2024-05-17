from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import users
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

auth = Blueprint('auth', __name__)

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

@auth.route("/profile")
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = users.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            flash('Logged in successfully!', category='success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Login unsuccessful. Check email and password.', category='error')
    return render_template('login.html', user=current_user, form=form)

@auth.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = form.password.data
        user = users.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        else:
            new_user = users(email=email, username=username, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            return redirect(url_for('main.dashboard'))
    return render_template('register.html', user=current_user, form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
