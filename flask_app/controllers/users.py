from flask import Flask, render_template, redirect, request, flash, session
from flask_app import app
from flask_app.models.user import User


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/clear_session")
def clear_session():
    session.clear()
    return redirect("/")



@app.route("/users/create", methods = ["POST"])
def create_user():
    print(request.form)
    if User.registry_validator(request.form):
        User.create(request.form)
    return redirect("/")

@app.route("/login", methods = ["POST"])
def login():
    if not User.login_validator(request.form):
        flash("invalid login")
        return redirect("/")

    user = User.get_by_email(request.form)

    session["user_id"] = user.id
    return redirect("/success")