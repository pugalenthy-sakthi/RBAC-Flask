from models.models import Activity
from sqlalchemy import and_


def create_activity(session,activity):
  
  try:
    session.add(activity)
    return True
  except Exception as e:
    return e
  
def get_activity(session_id):
  
  try:
    activity = Activity.query.filter(and_(Activity.session_id == session_id , Activity.logout_at == None)).first()
    return activity
  except Exception as e:
    return e

def update_activity(session,activity):
  
  try:
    session.add(activity)
    return True
  except Exception as e:
    return e
  