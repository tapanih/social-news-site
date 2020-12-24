import os
import pytest

os.environ["TEST"] = "test"

from application import app

@pytest.fixture
def client():
  return app.test_client()

def test_index(client):
  response = client.get("/")
  assert b"log in" in response.data
  assert b"register" in response.data
