from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint("auth", __name__)

@auth.route("/login", methods=['GET', 'POST'])
# @login_required
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash(f"Logged in {user.id}", category='success')
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Wrong password", category="error")
        else:
            flash("Email not found", category="error")

    return render_template("login.html")


@auth.route("/register", methods=['GET', 'POST'])
# @login_required
def register():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        confirmpassword = request.form.get("confirmpassword")
    
        email_exists = User.query.filter_by(email=email).first()

        if email_exists:
            flash("Email already registered", category='error')
        elif password != confirmpassword:
            flash("Passwords do not match", category='error')
        elif len(password) < 8:
            flash("Password is too short", category='error')
        else:
            new_user = User(email=email, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            #login_user(new_user, remember=True) loguje od razu po rejestracji usera
            flash("User created!", category='success')
            return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))