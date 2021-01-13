import config
from application import db
from application.models import Base
from sqlalchemy.sql import text
from datetime import datetime
from flask_login import current_user

class PostBase(Base):
  __abstract__ = True

  date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
  date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
      onupdate=db.func.current_timestamp())
  content = db.Column(db.String(config.TEXT_MAX_LENGTH), nullable=False)


class Post(PostBase):
  __tablename__ = "post"

  title = db.Column(db.String(config.TITLE_MAX_LENGTH), nullable=False)
  is_text = db.Column(db.Boolean, nullable=False)

  account_id = db.Column(db.Integer, db.ForeignKey('account.id'),
      nullable=False)
  
  # Also delete upvotes and comments when post is deleted
  upvotes = db.relationship("Upvote", cascade="delete")
  comments = db.relationship("Comment", cascade="delete")

  def __init__(self, title, is_text, content):
    self.title = title
    self.is_text = is_text
    self.content = content
  
  def upvotes(self):
    stmt = text("SELECT COUNT(account_id) FROM Upvote WHERE post_id = :post_id").params(post_id=self.id)
    res = db.engine.execute(stmt)
    return res.first()[0]

  @staticmethod
  def list_posts_ordered_by(param, page):
    user_id = current_user.id if current_user.is_authenticated else None
    field_name = "post_upvotes" if param == "upvote" else "post.date_created"

    stmt = text("SELECT post.id, post.date_created, post.content, "
                "post.title, post.is_text, "
                "(SELECT COUNT(*) FROM Upvote WHERE post_id = post.id) as post_upvotes, "
                "(SELECT COUNT(*) FROM Upvote WHERE post_id = post.id AND account_id = :user_id) as has_upvoted, "
                "account.username as post_author, "
                "COUNT(Comment.post_id) as post_comments FROM post "
                "LEFT JOIN Account ON Account.id = Post.account_id "
                "LEFT JOIN Comment ON Comment.post_id = Post.id "
                "GROUP BY Post.id, Account.id "
                "ORDER BY " + field_name + " DESC "
                "LIMIT :posts_per_page OFFSET ((:page - 1) * :posts_per_page);").params(
                  user_id=user_id, page=page, posts_per_page=config.POSTS_PER_PAGE
                )

    res = db.engine.execute(stmt)
    return [{"id":row[0], "date_created":datetime.fromisoformat(str(row[1])),
             "content":row[2], "title":row[3], "is_text":row[4], "upvotes":row[5],
             "current_user_has_upvoted":row[6], "author":row[7], "comments":row[8]}
              for row in res]

  @staticmethod
  def has_next(page):
    stmt = text("SELECT COUNT(*) FROM Post;")
    res = db.engine.execute(stmt)
    count = res.first()[0]
    return count > page * config.POSTS_PER_PAGE


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

  def __init__(self, account_id, post_id):
    self.account_id = account_id
    self.post_id = post_id