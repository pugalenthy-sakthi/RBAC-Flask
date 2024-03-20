from flask import jsonify
from http import HTTPStatus

response_body = {
    'data':{},
    'http_status':'',
    'message':''
}

def success_response_sender(data,message):
    return common_response_sender(data,message,HTTPStatus.OK)

def forbidden_response_sender(data,message):
    return common_response_sender(data,message,HTTPStatus.FORBIDDEN)

def bad_request_sender(data,message):
    return common_response_sender(data,message,HTTPStatus.BAD_REQUEST)

def not_found_sender(data,message):
    return common_response_sender(data,message,HTTPStatus.NOT_FOUND)

def created_response_sender(data,message):
    return common_response_sender(data,message,HTTPStatus.CREATED)

def server_error_sender(data,message):
    return common_response_sender(data,message,HTTPStatus.INTERNAL_SERVER_ERROR)

def conflict_error_sender(data,message):
    return common_response_sender(data,message,HTTPStatus.CONFLICT)
    
    
def common_response_sender(data,message,http_status:HTTPStatus):
    
    response_body['data'] = data
    response_body['http_status'] = http_status.phrase
    response_body['message'] = message
    
    return jsonify(response_body),http_status.value