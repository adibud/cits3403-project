from flask import Blueprint, render_template, request, redirect, url_for, request, flash
from flask_login import login_required, current_user, current_request
from .models import comments, requests, users
from . import db

main = Blueprint('main', __name__)

#default page users are directed to 
@main.route("/")
@login_required
def index():
    return render_template("home2.html", user=current_user)



@main.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        comment = request.form.get('comment')

        # Creates new comment with info from form
        new_comm = comments(comment=comment, user_id=current_user.id, request_id=current_request.id)

    #all_reqs displays all requests from all users
    all_reqs = requests.query.all()

    #all_comms displays all comments from all users 
    all_comms = comments.query.all()

    return render_template("home2.html", user=current_user, request=current_request, all_reqs=all_reqs, all_comms=all_comms)


@main.route("/create_request", methods=['GET', 'POST'])
@login_required
def create_request():
    if request.method == 'POST':
        title = request.form.get('title')
        descr = request.form.get('descr')
        quantity = request.form.get('quantity')
        
        # Creates new request instance with info from form 
        new_req = requests(title=title, descr=descr, quantity=quantity, user_id=current_user.id)
        
        # Adds new request to db session and commits
        db.session.add(new_req)
        db.session.commit()
        
        flash('Request posted!', category='success')

        

    return render_template("create_request.html", user=current_user)

@main.route("/dashboard")
@login_required
def dashboard():
    user_reqs = requests.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html", user=current_user, user_reqs=user_reqs)
