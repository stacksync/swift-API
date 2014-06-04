'''
Created on 05/03/2014

@author: Edgar Zamora Gomez
'''
from swift.common.swob import wsgify, HTTPForbidden, HTTPUnauthorized, HTTPBadRequest, HTTPNotFound,\
HTTPMethodNotAllowed, HTTPServerError

def create_error_response(error, message):
    if error == 400:
        response = HTTPBadRequest(body=message)
    elif error == 401:
        response = HTTPUnauthorized(body=message)
    elif error == 403:
        response = HTTPForbidden(body=message)
    elif error == 404:
        response = HTTPNotFound(body=message)
    elif error == 405:
        response = HTTPMethodNotAllowed(body=message)
    else:
        response = HTTPServerError(body=message)
        
    return response  