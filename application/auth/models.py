from application import db

class User(db.Model):

  __tablename__ = "account"

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(40), unique=True, nullable=False)
  password_hash = db.Column(db.String(255), nullable=False)
  date_registered = db.Column(db.DateTime, default=db.func.current_timestamp())

  threads = db.relationship("Thread", backref="author", lazy="dynamic")

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