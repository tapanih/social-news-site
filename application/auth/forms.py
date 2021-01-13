from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError
from application.auth.models import User
import config

class LoginForm(FlaskForm):
  username = StringField("username")
  password = PasswordField("password")

  class Meta:
    csrf = False

class RegisterForm(FlaskForm):
  username = StringField("username", validators=[
    Length(min=config.USERNAME_MIN_LENGTH, max=config.USERNAME_MAX_LENGTH,
           message=f"username must be between {config.USERNAME_MIN_LENGTH} " +
                    f"and {config.USERNAME_MAX_LENGTH} characters long")
  ])
  password = PasswordField("password", validators=[DataRequired()])
  confirm_password = PasswordField("confirm password",
    validators=[DataRequired(), EqualTo("password", "passwords do not match")])
  
  def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user:
      raise ValidationError("username taken")

  class Meta:
    csrf = False