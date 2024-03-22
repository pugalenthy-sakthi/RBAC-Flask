from flask import Blueprint,request
from schema.schemas import ApiData
from models.models import API
from database import api_service
from config import db
from marshmallow import ValidationError
from common import response_functions,responses
from sqlalchemy.exc import IntegrityError
import traceback

dev_route = Blueprint('dev_route',__name__,url_prefix='/api/dev')

@dev_route.post('/add/api')
def create_api():
  try:
    api_data = ApiData().load(request.json)
    session = db.session()
    api = API(api_name=api_data['api_name'],api_path=api_data['api_path'],method=api_data['method'])
    state = api_service.create_api(session,api)
    if state is True:
      session.commit()
      return response_functions.created_response_sender(None,responses.data_created)
  except IntegrityError as e:
    session.rollback()
    return response_functions.conflict_error_sender(None,responses.data_already_exist)
  except ValidationError as e:
    return response_functions.bad_request_sender(e.messages_dict,responses.invalid_data)
  except Exception as e:
    session.rollback()
    return response_functions.server_error_sender(None,responses.internal_server_error)


@dev_route.get('/get/api')
def get_all_api():
  try:
    api_list = api_service.get_all_api()
    api_data = [
      {
      'api_id':api.id,
      'api_name':api.api_name,
      'api_path':api.api_path,
      'api_method':api.method.value
      }
      for api in api_list
    ]
    return response_functions.success_response_sender(api_data,responses.data_success)
  except Exception as e:
    traceback.print_exception(e)
    return response_functions.server_error_sender(None,responses.internal_server_error)

