from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
import datetime  # Importing datetime module
from .models import requests, comments
from . import db
from .forms import CreateRequestForm, EditProfileForm

main = Blueprint('main', __name__)

@main.route("/")
def index():
    return render_template("home.html", user=current_user)

@main.route("/create_request", methods=['GET', 'POST'])
@login_required
def create_request():
    form = CreateRequestForm()
    if form.validate_on_submit():
        title = form.title.data
        descr = form.descr.data
        quantity = form.quantity.data
        image = form.image.data

        if image:
            filename = secure_filename(image.filename)
            upload_folder = os.path.join(current_app.root_path, 'static/uploads')
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            image_path = os.path.join(upload_folder, filename)
            image.save(image_path)
            file_url = url_for('static', filename='uploads/' + filename)
        else:
            file_url = None

        new_req = requests(title=title, descr=descr, quantity=quantity, image=file_url, user_id=current_user.id)
        db.session.add(new_req)
        db.session.commit()
        flash('Request posted!', category='success')
        return redirect(url_for('main.dashboard'))
    return render_template("create_request.html", user=current_user, form=form)

@main.route("/dashboard")
@login_required
def dashboard():
    user_reqs = requests.query.filter_by(user_id=current_user.id).all()
    for req in user_reqs:
        req.comments = comments.query.filter_by(request_id=req.id).all()
    return render_template("dashboard.html", user=current_user, user_reqs=user_reqs)


@main.route("/contact")
def contact():
    return render_template("contact.html", user=current_user)

@main.route("/edit_profile", methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your profile has been updated!', category='success')
        return redirect(url_for('main.dashboard'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template("edit_profile.html", user=current_user, form=form)

@main.route("/change_password")
@login_required
def change_password():
    return render_template("change_password.html", user=current_user)

@main.route("/add_comment/<int:request_id>", methods=['POST'])
@login_required
def add_comment(request_id):
    text = request.form.get('comment')
    if text:
        unique_text = f"{text} {datetime.datetime.now()}"  # Appending the current timestamp
        new_comment = comments(text=unique_text, commenter_id=current_user.id, request_id=request_id)
        db.session.add(new_comment)
        db.session.commit()
        flash('Comment added!', category='success')
    else:
        flash('Comment cannot be empty.', category='error')
    return redirect(url_for('main.dashboard'))

@main.route("/delete_request/<int:request_id>", methods=['POST'])
@login_required
def delete_request(request_id):
    req = requests.query.get_or_404(request_id)
    if req.user_id != current_user.id:
        flash('You do not have permission to delete this request.', category='error')
        return redirect(url_for('main.dashboard'))

    # Delete related comments first
    comments.query.filter_by(request_id=request_id).delete()
    db.session.delete(req)
    db.session.commit()
    flash('Request deleted!', category='success')
    return redirect(url_for('main.dashboard'))

@main.route("/edit_request/<int:request_id>", methods=['GET', 'POST'])
@login_required
def edit_request(request_id):
    req = requests.query.get_or_404(request_id)
    if req.user_id != current_user.id:
        flash('You do not have permission to edit this request.', category='error')
        return redirect(url_for('main.dashboard'))

    form = CreateRequestForm()
    if form.validate_on_submit():
        req.title = form.title.data
        req.descr = form.descr.data
        req.quantity = form.quantity.data
        image = form.image.data

        if image:
            filename = secure_filename(image.filename)
            upload_folder = os.path.join(current_app.root_path, 'static/uploads')
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            image_path = os.path.join(upload_folder, filename)
            image.save(image_path)
            req.image = url_for('static', filename='uploads/' + filename)

        db.session.commit()
        flash('Request updated!', category='success')
        return redirect(url_for('main.dashboard'))

    elif request.method == 'GET':
        form.title.data = req.title
        form.descr.data = req.descr
        form.quantity.data = req.quantity

    return render_template("edit_request.html", user=current_user, form=form, request_id=request_id)
