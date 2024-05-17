from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import requests
from . import db

main = Blueprint('main', __name__)

@main.route("/")
def index():
    return render_template("home.html", user=current_user)

@main.route("/create_request", methods=['GET', 'POST'])
@login_required
def create_request():
    if request.method == 'POST':
        title = request.form.get('title')
        descr = request.form.get('descr')
        quantity = request.form.get('quantity')
        image = request.form.get('image')
        if title and descr and quantity:
            new_req = requests(title=title, descr=descr, quantity=quantity, image=image, user_id=current_user.id)
            db.session.add(new_req)
            db.session.commit()
            flash('Request posted!', category='success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('All fields are required.', category='error')
    return render_template("create_request.html", user=current_user)

@main.route("/dashboard")
@login_required
def dashboard():
    user_reqs = requests.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html", user=current_user, user_reqs=user_reqs)

@main.route("/contact")
def contact():
    return render_template("contact.html", user=current_user)

@main.route("/edit_profile")
@login_required
def edit_profile():
    return render_template("edit_profile.html", user=current_user)

@main.route("/change_password")
@login_required
def change_password():
    return render_template("change_password.html", user=current_user)
