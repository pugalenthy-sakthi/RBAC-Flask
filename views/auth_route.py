from flask import Blueprint,request
from schema.schemas import SignupData,LoginData
from marshmallow import ValidationError
from common import response_functions,responses
from database import user_services,activity_service
from config import db
from models.models import User,Activity
from sqlalchemy.exc import IntegrityError
from utils.validations import check_password
from utils.generators import get_random_id
from flask_jwt_extended import create_access_token,create_refresh_token
import datetime


auth_route = Blueprint('auth_route',__name__,url_prefix='/api/auth')


@auth_route.post('/signup')
def user_signup():
  try:
    signup_data = SignupData().load(request.json)
    session = db.session()
    exist_data = user_services.get_user_by_email(signup_data['email'])
    if exist_data is None:
      user = User(name = signup_data['name'],password = signup_data['password'],email = signup_data['email'])
      state = user_services.create_user(session , user)
      if state is True : 
        session.commit()
        return response_functions.created_response_sender(None,responses.data_created)
    else :
      return response_functions.conflict_error_sender(None,responses.data_already_exist)
  except ValidationError as e:
    return response_functions.bad_request_sender(e.messages_dict,responses.invalid_data)
  except IntegrityError as e:
    session.rollback()
    return response_functions.conflict_error_sender(None,responses.data_already_exist)
  except Exception as e:
    session.rollback()
    return response_functions.server_error_sender(None,responses.internal_server_error)
  
@auth_route.post('/login')
def user_login():
  try:
    login_data = LoginData().load(request.json)
    session = db.session()
    exist_data = user_services.get_user_by_email(login_data['email'])
    if exist_data is None:
      return response_functions.not_found_sender(None,responses.data_not_found)
    else :
      if check_password(exist_data.password,login_data['password']) : 
        activity = Activity(exist_data)
        session_id = get_random_id()
        activity.session_id = session_id
        state = activity_service.create_activity(session,activity)
        if state : 
          session.commit()
          tokens = {
            'auth_token':create_access_token(identity=session_id),
            'refresh_token':create_refresh_token(identity=session_id)
          }
          return response_functions.success_response_sender(tokens,responses.login_response)
      else:
        return response_functions.forbidden_response_sender(None,responses.invalid_password)
  except ValidationError as e:
    return response_functions.bad_request_sender(e.messages_dict,responses.invalid_data)
  except IntegrityError as e:
    session.rollback()
    return response_functions.conflict_error_sender(None,responses.data_already_exist)
  except Exception as e:
    session.rollback()
    return response_functions.server_error_sender(None,responses.internal_server_error)
  
  
@auth_route.get('/refresh')
def user_refresh():
  try:
    session = db.session()
    session_id = request.headers['Session_Id']
    activity = activity_service.get_activity(session_id)
    if activity is None:
      return response_functions.not_found_sender(None,responses.data_not_found)
    user = activity.user
    new_activity = Activity(user)
    session_id = get_random_id()
    new_activity.session_id = session_id
    state = activity_service.create_activity(session,new_activity)
    if state : 
      session.commit()
      tokens = {
        'auth_token':create_access_token(identity=session_id),
        'refresh_token':create_refresh_token(identity=session_id)
      }
      return response_functions.success_response_sender(tokens,responses.data_success)
  except IntegrityError as e:
    session.rollback()
    return response_functions.conflict_error_sender(None,responses.data_already_exist)
  except Exception as e:
    session.rollback()
    print(e)
    return response_functions.server_error_sender(None,responses.internal_server_error)
  
@auth_route.get('/logout')
def user_logout():
  try:
    session = db.session()
    session_id = request.headers['Session_Id']
    activity = activity_service.get_activity(session_id)
    if activity is None:
      return response_functions.not_found_sender(None,responses.data_not_found)
    activity.logout_at = datetime.datetime.now()
    state = activity_service.update_activity(session,activity)
    if state :
      session.commit()
      return response_functions.success_response_sender(None,responses.data_success)
  except IntegrityError as e:
    session.rollback()
    return response_functions.conflict_error_sender(None,responses.data_already_exist)
  except Exception as e:
    session.rollback()
    return response_functions.server_error_sender(None,responses.internal_server_error)