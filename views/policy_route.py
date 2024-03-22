from flask import Blueprint,request
from models.models import Policy
from marshmallow import ValidationError
from schema.schemas import PolicyCreateData,PolicyApiData,PolicyUserData
from common import response_functions,responses
import traceback
from config import db
from database import policy_service,api_service,user_services
from sqlalchemy.exc import IntegrityError


policy_route = Blueprint('policy_route',__name__,url_prefix='/api/policy')


@policy_route.get('/')
def get_policies():
  try:
    policy_list = policy_service.get_all_policies()
    policies = [
      {
        'policy_id':policy.id,
        'policy_name':policy.policy_name,
        'allowed_api':[
          {
            'api_id':api.id,
            'api_path':api.api_path,
            'api_name':api.api_name,
            'api_method':api.method.value
          }
          for api in policy.api_list
        ]
      }
      for policy in policy_list
    ]
    return response_functions.success_response_sender(policies,responses.data_success)
  except Exception as e:
    traceback.print_exception(e)
    return response_functions.server_error_sender(None,responses.internal_server_error)
  
  
  
  

@policy_route.post('/create')
def create_policy():
  
  try:
    policy_data = PolicyCreateData().load(request.json)
    existing_data = policy_service.get_policy_by_name(policy_data['policy_name'])
    if existing_data is not None:
      return response_functions.conflict_error_sender(None,responses.data_already_exist)
    session = db.session()
    policy = Policy(policy_data['policy_name'])
    state = policy_service.create_policy(session,policy)
    if state is True:
      session.commit()
      return response_functions.created_response_sender(None,responses.data_created)
  except IntegrityError as e:
    session.rollback()
    return response_functions.conflict_error_sender(None,responses.data_already_exist)
  except ValidationError as e:
    return response_functions.bad_request_sender(e.messages_dict,responses.invalid_data)
  except Exception as e:
    traceback.print_exception(e)
    return response_functions.server_error_sender(None,responses.internal_server_error)
  
@policy_route.put('/add/apis')
def add_api():
  try:
    policy_api_data = PolicyApiData().load(request.json)
    session = db.session()
    policy:Policy = policy_service.get_policy(policy_api_data['policy_id'])
    if policy is None:
      return response_functions.not_found_sender(None,responses.data_not_found)
    api_list = policy.api_list
    new_apis = policy_api_data['api_ids']
    for api_id in new_apis:
      api = api_service.get_api(api_id)
      if api is None:
        session.close()
        return response_functions.not_found_sender(None,responses.data_not_found)
      if api in api_list:
        session.close()
        return response_functions.conflict_error_sender(None,responses.data_already_exist)
      api_list.append(api)
    policy.api_list = api_list
    state = policy_service.update_policy(session,policy)
    if state is True:
      session.commit()
      return response_functions.success_response_sender(None,responses.data_success)
  except IntegrityError as e:
    session.rollback()
    return response_functions.conflict_error_sender(None,responses.data_already_exist)
  except ValidationError as e:
    return response_functions.bad_request_sender(e.messages_dict,responses.invalid_data)
  except Exception as e:
    traceback.print_exception(e)
    return response_functions.server_error_sender(None,responses.internal_server_error)
  
  
@policy_route.put('/add/users')
def add_user():
  try:
    policy_user_data = PolicyUserData().load(request.json)
    session = db.session()
    policy:Policy = policy_service.get_policy(policy_user_data['policy_id'])
    if policy is None:
      return response_functions.not_found_sender(None,responses.data_not_found)
    users_list = policy.user_list
    new_users_list = policy_user_data['user_emails']
    for email in new_users_list:
      user = user_services.get_user_by_email(email)
      if user is None:
        session.close()
        return response_functions.not_found_sender(None,responses.data_not_found)
      if user in users_list:
        session.close()
        return response_functions.conflict_error_sender(None,responses.data_already_exist)
      users_list.append(user)
    policy.user_list = users_list
    state = policy_service.update_policy(session,policy)
    if state is True:
      session.commit()
      return response_functions.success_response_sender(None,responses.data_success)
  except IntegrityError as e:
    session.rollback()
    return response_functions.conflict_error_sender(None,responses.data_already_exist)
  except ValidationError as e:
    return response_functions.bad_request_sender(e.messages_dict,responses.invalid_data)
  except Exception as e:
    traceback.print_exception(e)
    return response_functions.server_error_sender(None,responses.internal_server_error)
