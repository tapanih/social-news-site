from application import db
from application.models import Base
from sqlalchemy.sql import text
from datetime import datetime

class PostBase(Base):
  __abstract__ = True

  date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
  date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
      onupdate=db.func.current_timestamp())
  content = db.Column(db.String(3000), nullable=False)


class Post(PostBase):
  __tablename__ = "post"

  title = db.Column(db.String(255), nullable=False)
  is_text = db.Column(db.Boolean, nullable=False)

  account_id = db.Column(db.Integer, db.ForeignKey('account.id'),
      nullable=False)
  
  upvoted_accounts = db.relationship("Upvote")

  def __init__(self, title, is_text, content):
    self.title = title
    self.is_text = is_text
    self.content = content
    self.upvotes = 0

  @staticmethod
  def list_posts_dangerously_ordered_by(param):
    stmt = text("SELECT post.id, post.date_created, post.content, "
                "post.title, post.is_text, (SELECT COUNT(*) FROM Upvote WHERE post_id = post.id) as post_upvotes, "
                "account.username as post_author, "
                "COUNT(Comment.post_id) as post_comments FROM post "
                "LEFT JOIN Account ON Account.id = Post.account_id "
                "LEFT JOIN Comment ON Comment.post_id = Post.id "
                "GROUP BY Post.id, Account.id "
                "ORDER BY " + param + " DESC;")

    res = db.engine.execute(stmt)
    return [{"id":row[0], "date_created":datetime.fromisoformat(str(row[1])),
             "content":row[2], "title":row[3], "is_text":row[4],
             "upvotes":row[5], "author":row[6], "comments":row[7]}
              for row in res]


class Comment(PostBase):

  post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
  account_id = db.Column(db.Integer, db.ForeignKey('account.id'),
      nullable=False)

  def __init__(self, content):
    self.content = content


class Upvote(db.Model):
  __tablename__ = "upvote"
  account_id = db.Column(db.Integer, db.ForeignKey('account.id'), primary_key=True)
  post_id = db.Column(db.Integer, db.ForeignKey('post.id'), primary_key=True)

  account = db.relationship("User",
      backref=db.backref("upvote", cascade="all, delete-orphan"))
  post = db.relationship("Post",
      backref=db.backref("upvote", cascade="all, delete-orphan"))

  def __init__(self, account_id, post_id):
    self.account_id = account_id
    self.post_id = post_id