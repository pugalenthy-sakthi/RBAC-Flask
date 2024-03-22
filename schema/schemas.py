from marshmallow import Schema,fields,validates,ValidationError
from utils.validations import validate_email,validate_name
from models.models import APIMethods
from common import responses


class SignupData(Schema):
  
  name = fields.String(required=True,allow_none=False,validate=validate_name)
  email = fields.String(required=True,allow_none=False,validate=validate_email)
  password = fields.String(required=True,allow_none=False)
  
  
class LoginData(Schema):
  
  email = fields.String(required=True,allow_none=False,validate=validate_email)
  password = fields.String(required=True,allow_none=False)
  
  
class ApiData(Schema):
  
  api_name = fields.String(required=True,allow_none=False)
  api_path = fields.String(required=True,allow_none=False)
  method = fields.Enum(APIMethods)
  
class PolicyCreateData(Schema):
  
  policy_name = fields.String(required=True,allow_none=False)
  
class PolicyApiData(Schema):
  
  policy_id = fields.Integer()
  api_ids = fields.List(fields.Integer(),required = True)
  
  @validates('api_ids')
  def validate_length(self,value):
    if len(value) == 0:
      raise ValidationError(responses.length_zero_error) 
    
    
class PolicyUserData(Schema):
  
  policy_id = fields.Integer()
  user_emails = fields.List(fields.String(),required = True)
  
  @validates('user_emails')
  def validate_length(self,value):
    if len(value) == 0:
      raise ValidationError(responses.length_zero_error) 
