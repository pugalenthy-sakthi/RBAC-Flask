from models.models import User,Activity
from config import db
from common import response_functions,responses
from utils import validations,generators
from flask_jwt_extended import create_access_token,create_refresh_token

def create_user(data):
  try:
    exist_data = User.query.filter_by(email = data['email']).first()
    if exist_data is None:
      user = User(data['name'],data['password'],data['email'])
      db.session.add(user)
      db.session.commit()
      return response_functions.created_response_sender(None,responses.data_created)
    else :
      return response_functions.conflict_error_sender(None,responses.data_already_exist)
  except Exception as e:
    return response_functions.server_error_sender(None,responses.internal_server_error)
  
  
def user_login(data):
  try:
    exist_data = User.query.filter_by(email = data['email']).first()
    if exist_data is not None:
      if validations.check_password(exist_data.password,data['password']):
        activity = Activity(exist_data)
        session_id = generators.get_random_id()
        activity.session_id = session_id
        db.session.add(activity)
        db.session.commit()
        tokens = {
          'auth_token':create_access_token(identity=session_id),
          'refresh_token':create_refresh_token(identity=session_id)
        }
        return response_functions.success_response_sender(tokens,responses.login_response)
        
      else:
        return response_functions.forbidden_response_sender(None,responses.invalid_password)
    else :
      return response_functions.not_found_sender(None,responses.data_not_found)
  except Exception as e:
    print(e)
    return response_functions.server_error_sender(None,responses.internal_server_error)
  