from flask import request
from flask_jwt_extended import decode_token
from database import activity_service,user_services
from common import responses,response_functions
from utils import caching
from models.models import User

open_paths = [
    '/api/auth/signup',
    '/api/auth/login',
    '/favicon.ico'
]
def token_required(*args,**kwargs):
  if request.path in open_paths:
      pass
  else:
    if 'Authorization' not in request.headers:
       return response_functions.forbidden_response_sender(None,responses.forbidden_response)
    else:
        token = request.headers['Authorization']
        try:
          data = decode_token(token)
          session_id = data['sub']
          user_activity = caching.get_activity_cache(session_id)
          session = None
          if user_activity == None :
            session = activity_service.get_activity(data['sub'])
            if session == None :
               return response_functions.forbidden_response_sender(None,responses.forbidden_response)
            caching.activity_cache(session,session_id)
            session = caching.get_activity_cache(session_id)
          else:
            session = user_activity
          if session['logout_at'] != 'None':
            return response_functions.forbidden_response_sender(None,responses.forbidden_response)
          request.environ['HTTP_USER_DATA'] = session['email']
          request.environ['HTTP_SESSION_ID'] = data['sub']
          
          user:User = user_services.get_user_by_email(session['email'])
          if user.isdev : 
            pass
          else:
            flag = False
            for policy in user.policy_list:
              for api in policy.api_list:
                if str(api.api_path).find(request.path) and api.method.value == request.method:
                  flag = True
                  break
              if flag:
                break
            if flag == False:
              return response_functions.forbidden_response_sender(None,responses.access_denied)
          
        except Exception as e:
          return response_functions.forbidden_response_sender(None,responses.forbidden_response)
