from application import db
from application.models import Base
from sqlalchemy.sql import text
from datetime import datetime

class PostBase(Base):
  __abstract__ = True

  date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
  date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
      onupdate=db.func.current_timestamp())
  content = db.Column(db.String(65536), nullable=False)

class Post(PostBase):
  __tablename__ = "post"

  title = db.Column(db.String(144), nullable=False)
  is_text = db.Column(db.Boolean, nullable=False)
  upvotes = db.Column(db.Integer, nullable=False)

  account_id = db.Column(db.Integer, db.ForeignKey('account.id'),
      nullable=False)
  
  upvoted_accounts = db.relationship("account", secondary="upvote")

  def __init__(self, title, is_text, content):
    self.title = title
    self.is_text = is_text
    self.content = content
    self.upvotes = 0

  @staticmethod
  def list_posts_dangerously_ordered_by(param):
    stmt = text("SELECT post.id, post.date_created, post.content, "
                "post.title, post.is_text, post.upvotes, "
                "account.username as post_author, "
                "COUNT(Comment.post_id) as post_comments FROM Post "
                "LEFT JOIN Account ON Account.id = Post.account_id "
                "LEFT JOIN Comment ON Comment.post_id = Post.id "
                "GROUP BY Post.id, Account.id "
                "ORDER BY " + param + " DESC;")

    res = db.engine.execute(stmt)
    return [{"id":row[0], "date_created":datetime.fromisoformat(row[1]),
             "content":row[2], "title":row[3], "is_text":row[4],
             "upvotes":row[5], "author":row[6], "comments":row[7]}
              for row in res]


class Comment(PostBase):

  post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
  account_id = db.Column(db.Integer, db.ForeignKey('account.id'),
      nullable=False)

  def __init__(self, content):
    self.content = content

class Upvote(Base):
  account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
  post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

  account = db.relationship("account",
      backref=db.backref("upvote", cascade="all, delete-orphan"))
  post = db.relationship("post",
      backref=db.backref("upvote", cascade="all, delete-orphan"))
