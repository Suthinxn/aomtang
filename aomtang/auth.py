from flask import Blueprint, render_template, url_for, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/register')
def register():
    return render_template("/register_page/register.html")


@auth.route("/login")
def login():
    return render_template("/login_page/login.html")



@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))