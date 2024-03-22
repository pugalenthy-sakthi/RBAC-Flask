from models.models import Policy

def create_policy(session,policy):
  
  try:
    session.add(policy)
    return True
  except Exception as e:
    return e
  
  
def get_policy(id):
  try:
    policy = Policy.query.filter(Policy.id == id).first()
    return policy
  except Exception as e:
    return e
  
def get_all_policies():
  
  try:
    policy_list = Policy.query.all()
    return policy_list
  except Exception as e:
    return e
  
def get_policy_by_name(name):
  
  try:
    policy = Policy.query.filter(Policy.policy_name == name).first()
    return policy
  except Exception as e:
    return e
  
  
def update_policy(session,policy):
  
  try:
    session.add(policy)
    return True
  except Exception as e:
    return e
  