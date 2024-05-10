from flask import Blueprint, render_template, request, redirect, url_for, request, flash
from .models import users
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)

@auth.route("/profile")
def profile():
    return render_template('profile.html')

#login working 
@auth.route("/login", methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        #scanning db if email exists 
        user = users.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash('Logged in successfully!', category='success')
            else:
                flash('Incorrect password!', category='error')
        else:
            flash('Email does not exist', category='error')
    
    return render_template("login.html", user=current_user)

#logout mechanisms working
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


#register working
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        username = request.form.get('username')


        #still need to update register constraints 
        user = users.query.filter_by(email=email).first()
        if user:
            flash('Email already in use', category='error')
        elif len(email) < 4:
            flash('Email not long enough', category="error")

        else:
            new_user = users(email=email, username=username, password=generate_password_hash(password, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()

            #logs in user as soon as they register 
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('auth.login')) 
        
    return render_template("register.html", user=current_user)
