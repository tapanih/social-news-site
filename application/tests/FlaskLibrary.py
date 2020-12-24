import os

os.environ["TEST"] = "test"

from application import app

class FlaskLibrary(object):
  def __init__(self):
    self.client = app.test_client()
    self.response = None

  def navigate_to(self, path):
    self.response = self.client.get(path)
  
  def page_contains(self, text):
    if bytes(text, "utf-8") not in self.response.data:
      raise AssertionError(f"Page did not contain '{text}'. Response was: {self.response.data}")
