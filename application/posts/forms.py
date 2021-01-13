from flask_wtf import FlaskForm
from wtforms import StringField 
from wtforms.validators import Length, Optional, URL, ValidationError
from wtforms.widgets import TextArea
import config

class PostFormBase(FlaskForm):
  title = StringField("title", validators=[
    Length(min=config.TITLE_MIN_LENGTH, max=config.TITLE_MAX_LENGTH,
           message=f"title must be between {config.TITLE_MIN_LENGTH} " +
                   f"and {config.COMMENT_MAX_LENGTH} characters long")
  ])

  class Meta:
    csrf = False

class PostForm(PostFormBase):
  url = StringField("url", validators=[
    Optional(), URL(message="invalid URL (leave blank for text post)")
  ])
  text = StringField("text", widget=TextArea(), validators=[
    Optional(), Length(max=config.TEXT_MAX_LENGTH)
  ])

class EditUrlPostForm(PostFormBase):
  content = StringField("url", validators=[URL(message="invalid URL")])


class EditTextPostForm(PostFormBase):
  content = StringField("text", widget=TextArea(), validators=[
    Length(max=config.TEXT_MAX_LENGTH,
           message=f"text must be under {config.TEXT_MAX_LENGTH} characters long")
  ])

class CommentForm(FlaskForm):
  content = StringField("Add comment", widget=TextArea(), validators=[
    Length(min=config.COMMENT_MIN_LENGTH, max=config.COMMENT_MAX_LENGTH,
           message=f"comment must be between {config.COMMENT_MIN_LENGTH} and " +
                   f"{config.COMMENT_MAX_LENGTH} characters long")
  ])

  class Meta:
    csrf = False

class EditCommentForm(FlaskForm):
  content = StringField("Edit comment", widget=TextArea(), validators=[
    Length(min=config.COMMENT_MIN_LENGTH, max=config.COMMENT_MAX_LENGTH,
           message=f"comment must be between {config.COMMENT_MIN_LENGTH} and " +
                   f"{config.COMMENT_MAX_LENGTH} characters long")
  ])

  class Meta:
    csrf = False