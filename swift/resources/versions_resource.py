'''
Created on 05/03/2014

@author: Edgar Zamora Gomez
'''
from swift.common.swob import HTTPCreated, HTTPOk
from swift.common.utils import split_path
from swift_server.util import create_error_response


def GET(request, api_library):
    try:    
        _, _,_, file_id, _, version = split_path(request.path, 5, 6, False)
    except:
        return create_error_response(400, "Some problem with path.")
    # if version alone return all versions metadata
    if not version:
        message = api_library.get_versions(1234, file_id)
        if not message:
            return create_error_response(404, "File or folder not found at the specified path:" + request.path)

        return HTTPOk(body=message)
    # if version/id return information about specific version
    message = api_library.get_metadata(1234, file_id, specific_version=version)
    if not message:
        return create_error_response(404, "File or folder not found at the specified path:" + request.path)

    return HTTPOk(body=message)
    '''
    The case /api/file/file_id/versions/version_id/data you can find in data_resource
    ''' 