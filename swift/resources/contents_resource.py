'''
Created on 05/03/2014

@author: Edgar Zamora Gomez
'''
from swift.common.utils import split_path
from swift.common.swob import HTTPOk
from swift_server.util import create_error_response

def GET(request, api_library):

    try:
        include_deleted = request.params.get('include_deleted')
        if not include_deleted:
            include_deleted = False
    except:
        include_deleted = False
    try:    
        _, _,_, folder_id, _ = split_path(request.path, 5, 5, False)
    except:
        return create_error_response(400, "Some problem with path")
    
    message = api_library.get_folder_contents(123, folder_id, include_deleted)
    if not message:
        return create_error_response(404, "File or folder not found at the specified path:" + request.path)

    return HTTPOk(body=message)