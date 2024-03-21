from models.models import User
from sqlalchemy import and_

def create_user(session,user):
  try:
    session.add(user)
    return True
  except Exception as e:
    return e
  
  
def get_user_by_email(email):
  
  try:
    exist_data = User.query.filter(and_(User.email == email,User.deleted_at == None)).first()
    return exist_data
  except Exception as e:
    return e
