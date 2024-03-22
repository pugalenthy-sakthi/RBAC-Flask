import uuid
from flask import request


def get_random_id():
  return uuid.uuid4().hex

def get_current_session():
  return request.headers['Session_Id']