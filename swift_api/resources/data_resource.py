'''
Created on 05/03/2014

@author: Edgar Zamora Gomez
'''
from swift.common.utils import split_path
from swift.common.swob import HTTPCreated, HTTPOk
from swift_server.util import create_error_response
import json, urlparse
from util import *
from data_handler import DataHandler
import magic

def PUT(request, api_library):

    #take parameters. In this case, the content for update the file
    args = urlparse.parse_qs(request.body, 1)
    try:
        content = args['content']
    except:
        return create_error_response(400, "Supervise parameters, you not put anything to update.")
    else:
        if not content:
            return create_error_response(400, "Supervise parameters, you not put anything to update.")


    try:
        _, _,_, file_id, _ = split_path(request.path, 5, 5, False)
    except:
        return create_error_response(400, "INCORRECT PARAMETERS", "Supervise parameters, the correct form is \
         api/file/file_id/data")

    # We look up the name of file, and full path, to update it.
    message = api_library.get_metadata(1234, file_id)
    if not message:
        return create_error_response(404, "File or folder not found at the specified path:" + request.path_info)

    message = json.loads(message)
    if "error" in message:
        # Create error response
        error = message["error"]
        response = create_error_response(error, str(json.dumps(message['description'])))
    else:
        response = HTTPCreated(body=str(json.dumps(message['metadata'])))
    # Create new version to save old content version
    #TODO: Define mimetype, size and chunk

    chunk_maker = BuildFile(content, [])
    chunk_maker.separate()

    url_base = request['PATH_INFO'].replace("/files/"+file_id+"/data", "")
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

    message_new_version = api_library.update_data(request.environ["stacksync_user_id"], message["id"], message["parent"], mimetype, file_size, chunks)
    if not message_new_version:
        return create_error_response(404, "Some problem to create a new version of file")

    # TODO: Using name and full path update the file into DB, using new version.
    data = json.loads(message_new_version)
    if "error" in data:
        # Create error response
        error = data["error"]
        response = create_error_response(error, str(json.dumps(data['description'])))
    else:
        response = HTTPCreated(body=str(json.dumps(data['metadata'])))

    return response

def GET(request, api_library):

    try:
        _, _,_, file_id, _, version, _ = split_path(request.path, 5, 7, False)
    except:
        return create_error_response(400, "INCORRECT PARAMETERS", "Supervise parameters, something is wrong")

    metadata = api_library.get_metadata(request.environ["stacksync_user_id"], file_id, include_chunks=True, specific_version=version)
    if not metadata:
            return create_error_response(404, "File or folder not found at the specified path:" + request.path)
    metadata_dict = json.loads(metadata)

    if "error" in metadata_dict:
        error = metadata_dict["error"]
        return create_error_response(error, metadata)

    url_base = request['PATH_INFO'].replace("/files/"+file_id+"/data", "")
    script_name = request['SCRIPT_NAME']
    request["QUERY_STRING"] = ""
    data_handler = DataHandler(request["APP"])

    file_compress_content, status = data_handler.get_chunks(request, url_base, script_name, metadata_dict['chunks'])

    if len(file_compress_content) > 0:
        join_file = BuildFile("", file_compress_content)
        join_file.join()
        return HTTPOk(body=join_file.content)
    elif len(metadata_dict['chunks']) == 0:
        return HTTPOk(body="")


    # TODO: using metadata, where we can find the name and path of file, return content of file with DB
    content = 'There are the content of specific version of file'

    return HTTPOk(body=content)


    """
            # Check if error key exist
        data = json.loads(message)
        if "error" in data:
            # Create error response
            error = data["error"]
            return self.__createErrorResponse(error, message)

        urlBase = self.env['PATH_INFO'].replace("/files", "")
        scriptName = self.env['SCRIPT_NAME']
        self.env['QUERY_STRING'] = ""

        fileCompressContent, status = self.__getChunks(self.env, urlBase, scriptName, data['chunks'])
        if(len(fileCompressContent) > 0):
            joinFile = BuildFile("", fileCompressContent)
            joinFile.join()
            return HTTPOk(body=joinFile.content)
        elif(len(data['chunks']) == 0):
            return HTTPOk(body="")


        if status == 401:
            return HTTPUnauthorized()
        else:
            return HTTPBadRequest()
    """


