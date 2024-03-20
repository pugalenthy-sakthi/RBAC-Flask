import re
from marshmallow import ValidationError
from config import bcrypt
def validate_name(name):
  
  name_pattern = r'^[a-zA-Z]+(?:\s[a-zA-Z]+)*$'
  if re.match(name_pattern,name):
    pass
  else:
    raise ValidationError('Invalid Name')
  
def validate_email(email):
  
  email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
  if re.match(email_pattern,email):
    pass
  else:
    raise ValidationError('Invalid Email')
  
def check_password(hash_pwd,pwd):
  return bcrypt.check_password_hash(hash_pwd,pwd)