'''
Created on 3/03/2014

@author: Edgar Zamora Gomez
'''
import urlparse

from swift.common.swob import HTTPCreated, HTTPOk
from swift.common.utils import split_path
from swift_server.util import create_error_response


def POST(request, api_library):
    try:
        args = urlparse.parse_qs(request.body, 1)
    except:
        return create_error_response(400, "Some problem with parameters.")
    
    try:
        parent = args.get('parent')
    except:
        parent = None
    try:
        name = args.get('name')
    except:
        name = None
        
    if not name:
        return create_error_response(400, "It's mandatory to enter a name.")

    message = api_library.post_metadata(1234, name, parent)
   
    #TODO: create a file using name of arguments
    
    #TODO: Ask TO Cristian when I need to use status 200 or 201
    return HTTPCreated(body=message)

def DELETE(request, api_library):
 
    try:
        _, _,_, file_id = split_path(request.path, 4, 4, False)
    except:
        return create_error_response(400, "It's mandatory to enter a file_id.")
    # get Metadata of the file that had been deleted
    message = api_library.delete_item(1234, file_id)


    return HTTPOk(body=message)

def GET(request, api_library):  

    try:
        _, _, _, file_id = split_path(request.path, 4, 4, False)
    except:
        return create_error_response(400, "It's mandatory to enter a file_id.")

    message = api_library.get_metadata(1234, file_id)
    
    if not message:
        return create_error_response(404, "File or folder not found at the specified path:" + request.path_info)

    return HTTPOk(body=message)
   
def PUT(request, api_library):

    try:
        _, _,_, file_id = split_path(request.path, 4, 4, False)
    except:
        return create_error_response(400, "It's mandatory to enter a file_id. ")
    try:
        args = urlparse.parse_qs(request.body, 1)
    except:
        return create_error_response(400, "Some problem with parameters.")
    try:
        parent = args.get('parent')
    except:
        parent = None
    try:
        name = args.get('name')
    except:
        name = None
    message = api_library.put_metadata(1234, file_id, name, parent)

    # TODO: Move file to different parent
    return HTTPCreated(body=message)


