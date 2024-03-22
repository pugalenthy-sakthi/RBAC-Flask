
from config import redis_client
from flask import jsonify
import json

from models.models import Activity

def activity_cache(activity:Activity,session_id:str):
    
    activity_dict = {
        "session_id":activity.session_id,
        "user_id":activity.user_id,
        "login_at":str(activity.login_at),
        "logout_at":str(activity.logout_at),
        "email":activity.user.email
    }

    jstr = (json.dumps(activity_dict))
    
    redis_client.set(session_id,jstr)
    
    
def get_activity_cache(session_id):
    jstr =  redis_client.get(session_id)
    
    if jstr is None :
        return jstr
    return json.loads(jstr)


def delete_activity_cache(session_id):
    redis_client.delete(session_id)
    