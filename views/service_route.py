from flask import Blueprint
from database import user_services
from common import response_functions,responses


service_route = Blueprint('service_route',__name__,url_prefix='/api/service')


@service_route.get('/get/users')
def get_all_users():
  try:
    users_list = user_services.get_all_users()
    users_data = [
      {
      'name':user.name,
      'email':user.email
      }
      for user in users_list
    ]
    return response_functions.success_response_sender(users_data,responses.data_success)
  except Exception as e:
    return response_functions.server_error_sender(None,responses.internal_server_error)