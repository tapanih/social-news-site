from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from application import app, db
from application import bcrypt
from application.auth.models import User
from application.auth.forms import LoginForm, RegisterForm

@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
  if request.method == "GET":
    return render_template("auth/login.html", form=LoginForm())
  
  form = LoginForm(request.form)

  user = User.query.filter_by(username=form.username.data).first()

  if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
    login_user(user)
    return redirect(url_for("posts_index"))

  return render_template("auth/login.html", form=form,
                         error="Wrong username or password")
  

@app.route("/auth/logout")
def auth_logout():
  logout_user()
  return redirect(url_for("posts_index"))


@app.route("/auth/register", methods = ["GET", "POST"])
def auth_register():
  if request.method == "GET":
    return render_template("auth/register.html", form=RegisterForm())
  
  form = RegisterForm()

  if not form.validate():
    return render_template("auth/register.html", form=form)
  
  password_hash = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
  user = User(form.username.data, password_hash)
  
  db.session().add(user)
  db.session().commit()

  return redirect(url_for("auth_login"))