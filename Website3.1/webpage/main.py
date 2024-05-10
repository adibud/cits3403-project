from flask import Blueprint, render_template, request, redirect, url_for, request, flash
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route("/")
@login_required
def home():
    return render_template("home.html", user=current_user)