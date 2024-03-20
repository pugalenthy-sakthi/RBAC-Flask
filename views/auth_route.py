from flask import Blueprint,request
from schema.schemas import SignupData,LoginData
from marshmallow import ValidationError
from common import response_functions,responses
from services import user_services

auth_route = Blueprint('auth_route',__name__,url_prefix='/auth/api/')


@auth_route.post('/signup')
def schemas():
  try:
    signup_data = SignupData().load(request.json)
    return user_services.create_user(signup_data)
  except ValidationError as e:
    return response_functions.bad_request_sender(e.messages_dict,responses.invalid_data)
  
@auth_route.post('/login')
def login():
  try:
    login_data = LoginData().load(request.json)
    return user_services.user_login(login_data)
  except ValidationError as e:
    return response_functions.bad_request_sender(e.messages_dict,responses.invalid_data)
    