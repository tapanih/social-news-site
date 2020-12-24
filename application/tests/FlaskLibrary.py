import os

os.environ["TEST"] = "test"

from application import app

class FlaskLibrary(object):
  def __init__(self):
    self.client = app.test_client()
    self.response = None

  def navigate_to(self, path):
    self.response = self.client.get(path)
    if self.response.status_code != 200:
      raise AssertionError(f"Unexpected status code: {self.response.status_code} (expected: 200).")
  
  def page_contains(self, text):
    if bytes(text, "utf-8") not in self.response.data:
      raise AssertionError(f"Page did not contain '{text}'. Response was: {self.response.data}")

  def login(self, username, password):
    self.response = self.client.post('/auth/login', data=dict(
      username=username,
      password=password
    ), follow_redirects=True)

  def register(self, username, password, confirm_password):
    self.response = self.client.post("/auth/register", data=dict(
      username=username,
      password=password,
      confirm_password=confirm_password
    ), follow_redirects=True)
