from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from webpage.models import Request, Comment, Badge, User
from . import db
from webpage.forms import CreateRequestForm, EditProfileForm, ChangePasswordForm

# Create a Blueprint named 'main' for core application routes
main = Blueprint('main', __name__)

# Route for the homepage
@main.route("/")
def index():
    return render_template("home.html", user=current_user)

# Function to award badges to users
def award_badge(user, badge_name, description):
    if not Badge.query.filter_by(user_id=user.id, name=badge_name).first():
        badge = Badge(name=badge_name, description=description, user_id=user.id)
        db.session.add(badge)
        db.session.commit()

# Route to create a new request
@main.route("/create_request", methods=['GET', 'POST'])
@login_required
def create_request():
    form = CreateRequestForm()
    if form.validate_on_submit():
        title = form.title.data
        descr = form.descr.data
        image = form.image.data

        if image:
            filename = secure_filename(image.filename)
            upload_folder = os.path.join(current_app.root_path, 'static/uploads')
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            image_path = os.path.join(upload_folder, filename)
            image.save(image_path)
            file_url = 'uploads/' + filename
        else:
            file_url = None

        new_req = Request(title=title, descr=descr, image=file_url, user_id=current_user.id)
        db.session.add(new_req)
        if current_user.points is None:
            current_user.points = 0
        current_user.points += 10  # Award points for creating a request
        assign_badges(current_user)  # Assign badges based on points
        db.session.commit()
        flash('Request posted!', category='success')
        return redirect(url_for('main.dashboard'))
    return render_template("create_request.html", user=current_user, form=form)

# Route for the dashboard, displaying all requests and user information
@main.route("/dashboard")
@login_required
def dashboard():
    all_reqs = Request.query.all()
    for req in all_reqs:
        req.comments = Comment.query.filter_by(request_id=req.id).all()
        for comment in req.comments:
            comment.author = User.query.get(comment.commenter_id)
            comment.author.badges = Badge.query.filter_by(user_id=comment.commenter_id).all()
    
    users = User.query.order_by(User.points.desc()).all()  # Get all users sorted by points
    
    return render_template("dashboard.html", user=current_user, user_reqs=all_reqs, users=users)

# Route for the contact page
@main.route("/contact")
def contact():
    return render_template("contact.html", user=current_user)

@main.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    edit_profile_form = EditProfileForm()

    if request.method == 'POST':
        if edit_profile_form.validate_on_submit():
            current_user.username = edit_profile_form.username.data
            current_user.email = edit_profile_form.email.data
            current_user.bio = edit_profile_form.bio.data

            # Handle profile picture upload
            profile_picture = edit_profile_form.profile_picture.data
            if profile_picture:
                filename = secure_filename(profile_picture.filename)
                profile_pic_dir = os.path.join(current_app.root_path, 'static/profile_pics')
                if not os.path.exists(profile_pic_dir):
                    os.makedirs(profile_pic_dir)
                profile_picture.save(os.path.join(profile_pic_dir, filename))
                current_user.profile_picture = 'profile_pics/' + filename

            db.session.commit()
            flash('Your profile has been updated!', category='success')
            return redirect(url_for('main.profile'))

    elif request.method == 'GET':
        edit_profile_form.username.data = current_user.username
        edit_profile_form.email.data = current_user.email
        edit_profile_form.bio.data = current_user.bio

    user_reqs = Request.query.filter_by(user_id=current_user.id).all()
    return render_template("profile.html", user=current_user, form=edit_profile_form, user_reqs=user_reqs, badges=current_user.badges)


# Route to change the user's password
@main.route("/change_password", methods=['POST'])
@login_required
def change_password():
    password_form = ChangePasswordForm()
    edit_profile_form = EditProfileForm()

    if password_form.validate_on_submit():
        if check_password_hash(current_user.password, password_form.old_password.data):
            current_user.password = generate_password_hash(password_form.new_password.data, method='pbkdf2:sha256')
            db.session.commit()
            flash('Your password has been updated!', category='success')
        else:
            flash('Old password is incorrect.', category='error')

    user_reqs = Request.query.filter_by(user_id=current_user.id).all()
    return render_template("profile.html", user=current_user, edit_profile_form=edit_profile_form, password_form=password_form, user_reqs=user_reqs)

# Route to add a comment to a request
@main.route("/add_comment/<int:request_id>", methods=['POST'])
@login_required
def add_comment(request_id):
    text = request.form.get('comment')
    if text:
        new_comment = Comment(text=text, commenter_id=current_user.id, request_id=request_id)
        db.session.add(new_comment)
        db.session.commit()
        flash('Comment added!', category='success')
    else:
        flash('Comment cannot be empty.', category='error')
    return redirect(url_for('main.dashboard'))

@main.route("/delete_request/<int:request_id>", methods=['POST'])
@login_required
def delete_request(request_id):
    req = Request.query.get_or_404(request_id)
    if req.user_id != current_user.id:
        flash('You do not have permission to delete this request.', category='error')
        return redirect(url_for('main.dashboard'))

    Comment.query.filter_by(request_id=request_id).delete()
    db.session.delete(req)
    db.session.commit()
    flash('Request deleted!', category='success')
    return redirect(url_for('main.dashboard'))

# Route to edit a request
@main.route("/edit_request/<int:request_id>", methods=['GET', 'POST'])
@login_required
def edit_request(request_id):
    req = Request.query.get_or_404(request_id)
    if req.user_id != current_user.id:
        flash('You do not have permission to edit this request.', category='error')
        return redirect(url_for('main.dashboard'))

    form = CreateRequestForm()
    if form.validate_on_submit():
        req.title = form.title.data
        req.descr = form.descr.data
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

    return render_template("edit_request.html", user=current_user, form=form, request_id=request_id)

# Route for the leaderboard page
@main.route("/leaderboard")
@login_required
def leaderboard():
    users = User.query.order_by(User.points.desc()).all()
    return render_template("leaderboard.html", users=users)

# Route to delete a comment
@main.route('/delete_comment/<int:comment_id>', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    req = Request.query.get(comment.request_id)
    if comment.commenter_id == current_user.id or req.user_id == current_user.id:
        db.session.delete(comment)
        db.session.commit()
        flash('Comment deleted successfully', 'success')
    else:
        flash('You are not authorized to delete this comment', 'danger')
    return redirect(url_for('main.dashboard'))

# Dictionary for badge thresholds based on points
BADGE_THRESHOLDS = {
    "Common": {"points": 10, "icon": "common.png"},
    "Uncommon": {"points": 50, "icon": "uncommon.png"},
    "Rare": {"points": 100, "icon": "rare.png"},
    "Legendary": {"points": 200, "icon": "legendary.png"}
}

# Function to assign badges to users based on their points
def assign_badges(user):
    user.badges.clear()
    for badge_name, threshold in BADGE_THRESHOLDS.items():
        if user.points >= threshold["points"]:
            badge = Badge.query.filter_by(name=badge_name).first()
            if not badge:
                badge = Badge(name=badge_name, description=f"Earned {badge_name} badge", icon=threshold["icon"])
                db.session.add(badge)
            user.badges.append(badge)
    db.session.commit()
