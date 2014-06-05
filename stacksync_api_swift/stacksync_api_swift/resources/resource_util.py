import json
from swift.common.swob import Response, HTTPForbidden, HTTPUnauthorized, HTTPBadRequest, HTTPNotFound, \
    HTTPMethodNotAllowed, HTTPServerError


def create_response(message, status_code=200):
    try:
        json_message = json.loads(message)
    except:
        return create_error_response(500, "Server error. Please contact an administrator.")

    if 'error' in json_message:
        error_code = json_message["error"]
        description = json_message["description"]
        return create_error_response(error_code, description)
    else:
        return Response(status=status_code, body=message)


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


def is_valid_status(status_code):
    return 200 <= status_code < 300