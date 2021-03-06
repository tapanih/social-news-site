from flask import Flask, redirect, request
from flask_bcrypt import Bcrypt
from flask_moment import Moment
app = Flask(__name__)
bcrypt = Bcrypt(app)
moment = Moment(app)

from flask_sqlalchemy import SQLAlchemy

import os

if os.environ.get("HEROKU"):
  app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
elif os.environ.get("TEST"):
  app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
  app.config["TESTING"] = True
else:
  app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///application.db"
  app.config["SQLALCHEMY_ECHO"] = True

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

from application import models

from application.helpers import views

from application.posts import models
from application.posts import views

from application.auth import models
from application.auth import views

from application.auth.models import User
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Please login to use this functionality."

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(user_id)


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/auth/login?next=' + request.path)


db.create_all()
