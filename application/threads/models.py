from application import db

class Thread(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
  date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                            onupdate=db.func.current_timestamp())

  title = db.Column(db.String(144), nullable=False)
  is_text = db.Column(db.Boolean, nullable=False)
  content = db.Column(db.String(65536), nullable=False)
  upvotes = db.Column(db.Integer, nullable=False)

  account_id = db.Column(db.Integer, db.ForeignKey('account.id'),
                         nullable=False)

  def __init__(self, title, is_text, content):
    self.title = title
    self.is_text = is_text
    self.content = content
    self.upvotes = 0
