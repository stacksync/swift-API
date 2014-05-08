'''
Created on 3/03/2014

@author: Edgar Zamora Gomez
'''
import json, urlparse
from util import *
from data_handler import DataHandler
import magic
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
    try:
        content = args.get('content')
    except:
        content = None

    if not name:
        return create_error_response(400, "It's mandatory to enter a name.")

    file_size = len(content)

    if file_size > 0:
        chunk_maker = BuildFile(content, [])
        chunk_maker.separate()

        url_base = request['PATH_INFO'].replace("/data", "")
        script_name = request['SCRIPT_NAME']
        data_handler = DataHandler(request["APP"])
        response = data_handler.upload_file_chunks(request, url_base, script_name, chunk_maker)

        chunks = chunk_maker.hashesList
        checksum = str((zlib.adler32(content) & 0xffffffff))
        file_size = str(len(content))
        mimetype = magic.from_buffer(content, mime=True)
        status = response.status_int
        if 200 > status >= 300:
            return response

        message_new_version = api_library.post_metadata(1234, name, parent, checksum, file_size, mimetype, chunks)

        if not message_new_version:
            return create_error_response(404, "Some problem to create a new file")

        # TODO: Using name and full path update the file into DB, using new version.
        data = json.loads(message_new_version)
        if "error" in data:
            # Create error response
            error = data["error"]
            response = create_error_response(error, str(json.dumps(data['description'])))
        else:
            response = HTTPCreated(body=str(json.dumps(data['metadata'])))

        return response

    '''Without content'''
    message = api_library.post_metadata(request.get("stacksync_user_id"), name, parent, None, 0, None, None)
    data = json.loads(message)
    if "error" in data:
        # Create error response
        error = data["error"]
        response = create_error_response(error, str(json.dumps(data['description'])))
    else:
        response = HTTPCreated(body=message)
    #TODO: create a file using name of arguments

    #TODO: Ask TO Cristian when I need to use status 200 or 201
    return response
def DELETE(request, api_library):

    try:
        _, _,_, file_id = split_path(request.path, 4, 4, False)
    except:
        return create_error_response(400, "It's mandatory to enter a file_id.")
    # get Metadata of the file that had been deleted
    message = api_library.delete_item(request.get("stacksync_user_id"), file_id)


    return HTTPOk(body=message)

def GET(request, api_library):

    try:
        _, _, _, file_id = split_path(request.path, 4, 4, False)
    except:
        return create_error_response(400, "It's mandatory to enter a file_id.")

    message = api_library.get_metadata(request.get("stacksync_user_id"), file_id)

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
    message = api_library.put_metadata(request.get("stacksync_user_id"), file_id, name, parent)

    # TODO: Move file to different parent
    return HTTPCreated(body=message)