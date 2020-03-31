from flask_wtf import FlaskForm
from wtforms import StringField 
from wtforms.validators import Length, Optional, URL, ValidationError

class PostForm(FlaskForm):
  title = StringField("title", validators=[Length(min=2, max=255)])
  url = StringField("url", validators=[Optional(), URL(message="Invalid URL. Leave blank for text post.")])
  text = StringField("text", validators=[Optional(), Length(max=65500)])

  class Meta:
    csrf = False

class EditUrlPostForm(FlaskForm):
  title = StringField("title", validators=[Length(min=2, max=255)])
  content = StringField("url", validators=[URL(message="Invalid URL")])

  class Meta:
    csrf = False

class EditTextPostForm(FlaskForm):
  title = StringField("title", validators=[Length(min=2, max=255)])
  content = StringField("text", validators=[Length(max=65500)])

  class Meta:
    csrf = False

class CommentForm(FlaskForm):
  content = StringField("text", validators=[Length(min=2, max=65500)])

  class Meta:
    csrf = False