from models.models import API
from sqlalchemy import and_

def create_api(session,api):
  try:
    session.add(api)
    return True
  except Exception as e:
    return e

def get_all_api():
  try:
    api_list = API.query.all()
    return api_list
  except Exception as e:
    return e
  
  
def get_user_api():
  
  try:
    api_list = API.query.filter(and_(not API.api_path.contains('/admin/'),not API.api_path.constraints('/dev/'))).all()
    return api_list
  except Exception as e:
    return e
  
def get_admin_api():
  
  try:
    api_list = API.query.filter(not API.api_path.constraints('/dev/')).all()
    return api_list
  except Exception as e:
    return e
  
def get_api(id):
  
  try:
    api = API.query.filter(API.id == id).first()
    return api
  except Exception as e:
    return e