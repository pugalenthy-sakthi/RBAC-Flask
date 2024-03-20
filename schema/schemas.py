from marshmallow import Schema,fields
from utils.validations import validate_email,validate_name

class SignupData(Schema):
  
  name = fields.String(required=True,allow_none=False,validate=validate_name)
  email = fields.String(required=True,allow_none=False,validate=validate_email)
  password = fields.String(required=True,allow_none=False)
  
  
class LoginData(Schema):
  
  email = fields.String(required=True,allow_none=False,validate=validate_email)
  password = fields.String(required=True,allow_none=False)