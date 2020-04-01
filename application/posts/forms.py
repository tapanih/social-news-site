from flask_wtf import FlaskForm
from wtforms import StringField 
from wtforms.validators import Length, Optional, URL, ValidationError
from wtforms.widgets import TextArea

class PostForm(FlaskForm):
  title = StringField("title", validators=[Length(min=2, max=255)])
  url = StringField("url", validators=[Optional(), URL(message="Invalid URL. Leave blank for text post.")])
  text = StringField("text", widget=TextArea(), validators=[Optional(), Length(max=65500)])

  class Meta:
    csrf = False

class EditUrlPostForm(FlaskForm):
  title = StringField("title", validators=[Length(min=2, max=255)])
  content = StringField("url", validators=[URL(message="Invalid URL")])

  class Meta:
    csrf = False

class EditTextPostForm(FlaskForm):
  title = StringField("title", validators=[Length(min=2, max=255)])
  content = StringField("text", widget=TextArea(), validators=[Length(max=65500)])

  class Meta:
    csrf = False

class CommentForm(FlaskForm):
  content = StringField("Add comment", widget=TextArea(), validators=[Length(min=2, max=65500)])

  class Meta:
    csrf = False