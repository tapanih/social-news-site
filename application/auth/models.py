from application import db
from application.models import Base
from sqlalchemy.sql import text

class User(Base):

  __tablename__ = "account"

  username = db.Column(db.String(40), unique=True, nullable=False)
  password_hash = db.Column(db.String(255), nullable=False)
  date_registered = db.Column(db.DateTime, default=db.func.current_timestamp())

  posts = db.relationship("Post", backref="author", lazy="dynamic")
  comments = db.relationship("Comment", backref="author", lazy="dynamic")

  def __init__(self, username, password_hash):
    self.username = username
    self.password_hash = password_hash
  
  def get_id(self):
    return self.id

  def is_active(self):
    return True

  def is_anonymous(self):
    return False

  def is_authenticated(self):
    return True

  def get_karma(self):
    stmt = text("SELECT SUM(post.upvotes) FROM post "
                "WHERE post.account_id == :user_id").params(user_id=self.id)
    res = db.engine.execute(stmt)
    for row in res:
      return row[0]