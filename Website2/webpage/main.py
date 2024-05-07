from flask import Blueprint, render_template, request, redirect, url_for, request, flash

main = Blueprint('main', __name__)

@main.route("/home")
def homepage():
    return render_template("base.html")