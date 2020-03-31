from application import db
from application.models import Base

class PostBase(Base):
  __abstract__ = True

  date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
  date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
      onupdate=db.func.current_timestamp())
  content = db.Column(db.String(65536), nullable=False)

class Post(PostBase):

  title = db.Column(db.String(144), nullable=False)
  is_text = db.Column(db.Boolean, nullable=False)
  upvotes = db.Column(db.Integer, nullable=False)

  account_id = db.Column(db.Integer, db.ForeignKey('account.id'),
      nullable=False)

  def __init__(self, title, is_text, content):
    self.title = title
    self.is_text = is_text
    self.content = content
    self.upvotes = 0

class Comment(PostBase):

  post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
  account_id = db.Column(db.Integer, db.ForeignKey('account.id'),
      nullable=False)

  def __init__(self, content):
    self.content = content
