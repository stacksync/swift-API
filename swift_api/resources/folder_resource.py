'''
Created on 3/03/2014

@author: Edgar Zamora Gomez
'''
import urlparse

from swift.common.swob import HTTPCreated, HTTPOk
from swift.common.utils import split_path
from swift_server.util import create_error_response


def POST(request, api_library, app):
    try:
        args = urlparse.parse_qs(request.body, 1)
    except:
        return create_error_response(400, "Some problem with parameters.")
  
    try:
        parent = args.get('parent')[0]
    except:
        parent = None
    try:
        name = args.get('name')[0]
    except:
        name = None
        
    if not name:
        return create_error_response(400, "It's mandatory to enter a folder_id.")
    
    message = api_library.new_folder(request.environ["stacksync_user_id"], name, parent)

    return HTTPCreated(body=message)

def DELETE(request, api_library, app):

    try:    
        _, _, folder_id = split_path(request.path, 3, 3, False)
    except:
        return create_error_response(400, "It's mandatory to enter a folder_id.")
    
    message = api_library.delete_item(request.environ["stacksync_user_id"], folder_id)
    if not message:
        return create_error_response(404, "File or folder not found at the specified path:" + request.path_info)

    return HTTPOk(body=message)

def GET(request, api_library, app):

    try:    
        _, _, folder_id = split_path(request.path, 2, 3, False)
    except:
        return create_error_response(400, "It's mandatory to enter a file_id.")


    message = api_library.get_metadata(request.environ["stacksync_user_id"], folder_id)

    if not message:
        return create_error_response(404, "File or folder not found at the specified path:" + request.path_info)
           

    return HTTPOk(body=message)

def PUT(request, api_library, app):

#     args = http.parse_qs(request.content.read(), 1)
    try:
        _, _, folder_id = split_path(request.path, 3, 3, False)
    except:
        return create_error_response(400, "It's mandatory to enter a file_id.")
    try:
        args = urlparse.parse_qs(request.body, 1)
    except:
        return create_error_response(400, "Some problem with parameters.")
    try:
        parent = args.get('parent')[0]
    except:
        parent = None
    try:
        name = args.get('name')[0]
    except:
        name = None
        
    message = api_library.put_metadata(request.environ["stacksync_user_id"], folder_id, name, parent)

    return HTTPCreated(body=message)
