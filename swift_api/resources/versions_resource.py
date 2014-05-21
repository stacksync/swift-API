'''
Created on 05/03/2014

@author: Edgar Zamora Gomez
'''
from swift.common.swob import HTTPCreated, HTTPOk
from swift.common.utils import split_path
from swift_server.util import create_error_response
import json


def GET(request, api_library, app):
    try:    
        _, _, file_id, _, version = split_path(request.path, 4, 5, False)
    except:
        return create_error_response(400, "Some problem with path.")
    # if version alone return all versions metadata
    if not version:
        message = api_library.get_versions(request.environ["stacksync_user_id"], file_id)
        data = json.loads(message)
        if "error" in data:
            error = data['error']
            return create_error_response(error, str(json.dumps(data['description'])))
        else:
            return HTTPOk(body=message)
    # if version/id return information about specific version
    message = api_library.get_metadata(request.environ["stacksync_user_id"], file_id, specific_version=version)
    data = json.loads(message)
    if "error" in data:
        error = data['error']
        return create_error_response(error, str(json.dumps(data['description'])))
    else:
        return HTTPOk(body=message)

    '''
    The case /v1/file/file_id/versions/version_id/data you can find in data_resource
    ''' 