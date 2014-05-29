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


def PUT(request, api_library, app):
    #take parameters. In this case, the content for update the file

    content = request.body
    if len(content) == 0:
        app.logger.error("StackSync API: data_resource PUT: error: %s content length: 0", str(400))
        return create_error_response(400, "Supervise parameters, you not put anything to update.")

    try:
        _, _, file_id, _ = split_path(request.path, 4, 4, False)
    except:
        app.logger.error("StackSync API: data_resource PUT: error: %s path_info: %s", str(400),
                         str(request.path_info))
        return create_error_response(400, "INCORRECT PARAMETERS", "Supervise parameters, the correct form is \
         api/file/file_id/data")

    app.logger.info('StackSync API: data_resource PUT: path info: %s content length: %i ', str(request.path_info),
                    len(content))

    # We look up the name of file, and full path, to update it.
    message = api_library.get_metadata(request.environ["stacksync_user_id"], file_id)
    if not message:
        app.logger.error("StackSync API: data_resource PUT: error: %s path info: %s", str(400), str(request.path_info))
        return create_error_response(404, "File or folder not found at the specified path:" + request.path_info)

    message = json.loads(message)
    if "error" in message:
        # Create error response
        error = message["error"]
        response = create_error_response(error, str(json.dumps(message['description'])))
        app.logger.error('StackSync API: data_resource PUT: status: %s description: %s', str(error),
                        str(message['description']))
    else:
        response = HTTPCreated(body=message)

    chunk_maker = BuildFile(content, [])
    chunk_maker.separate()

    url_base = request.environ['PATH_INFO'].replace("/file/" + file_id + "/data", "")
    script_name = request.environ['SCRIPT_NAME']
    data_handler = DataHandler(app)

    container_response = api_library.get_workspace_info(request.environ["stacksync_user_id"], message["id"])
    container_response = json.loads(container_response)
    if 'error' in container_response:
        error = container_response["error"]
        app.logger.error('StackSync API: data_resource PUT: status: %s description: %s', str(error),
                        str(container_response['description']))
        return create_error_response(error, str(json.dumps(container_response['description'])))

    response = data_handler.upload_file_chunks(request.environ, url_base, chunk_maker,
                                               container_response['swift_container'])

    chunks = chunk_maker.hashesList
    checksum = str((zlib.adler32(content) & 0xffffffff))
    file_size = str(len(content))
    mimetype = magic.from_buffer(content, mime=True)
    status = response.status_int
    if 200 <= status < 300:
        app.logger.error("StackSync API: data_resource PUT: error: %s path info: %s", str(response.status),
                         str(request.path_info))

        return response

    message_new_version = api_library.update_data(request.environ["stacksync_user_id"], message["id"], checksum,
                                                  file_size, mimetype, chunks)


    # TODO: Using name and full path update the file into DB, using new version.
    data = json.loads(message_new_version)
    if "error" in data:
        # Create error response
        error = data["error"]
        response = create_error_response(error, str(json.dumps(data['description'])))
        app.logger.error('StackSync API: data_resource PUT: status: %s description: %s', str(error),
                        str(data['description']))
    else:
        response = HTTPCreated(body=str(json.dumps(data['metadata'])))

    return response


def GET(request, api_library, app):
    try:
        _, _, file_id, _, version, _ = split_path(request.path, 4, 6, False)
    except:
        return create_error_response(400, "INCORRECT PARAMETERS", "Supervise parameters, something is wrong")
    app.logger.info('StackSync API: data_resource GET: path info: %s ', str(request.path_info))
    metadata = api_library.get_metadata(request.environ["stacksync_user_id"], file_id, include_chunks=True,
                                        specific_version=version)
    if not metadata:
        return create_error_response(404, "File or folder not found at the specified path:" + request.path)
    metadata_dict = json.loads(metadata)

    if "error" in metadata_dict:
        error = metadata_dict["error"]
        app.logger.error('StackSync API: data_resource PUT: status: %s description: %s', str(error),
                        str(metadata_dict['description']))
        return create_error_response(error, metadata)

    url_base = request.environ['PATH_INFO'].replace("/file/" + file_id + "/data", "")
    data_handler = DataHandler(app)

    container_response = api_library.get_workspace_info(request.environ["stacksync_user_id"], metadata_dict["id"])
    container_response = json.loads(container_response)
    if 'error' in container_response:
        error = container_response["error"]
        app.logger.error('StackSync API: data_resource PUT: status: %s description: %s', str(error),
                        str(container_response['description']))

        return create_error_response(error, str(json.dumps(container_response['description'])))

    file_compress_content, status = data_handler.get_chunks(request.environ, url_base, metadata_dict['chunks'],
                                                            container_response['swift_container'])

    if 200 <= status < 300:
        if len(file_compress_content) > 0:
            join_file = BuildFile("", file_compress_content)
            join_file.join()
            headers = {'Content-Type': metadata_dict['mimetype']}
            return HTTPOk(body=join_file.content, headers=headers)
        elif len(metadata_dict['chunks']) == 0:
            return HTTPOk(body="")
    else:
        return create_error_response(status, "Error: Not be able to return Chunks")






