from swift.common.utils import split_path
from swift.common.swob import HTTPOk
from stacksync_api_swift.resources.data_util import BuildFile
from stacksync_api_swift.resources.resource_util import create_response, is_valid_status, create_error_response
from stacksync_api_swift.resources.data_handler import DataHandler
import magic
import json
import zlib


def PUT(request, api_library, app):
    """
    PUT /file/:file_id/data

    Upload file data

    An application can upload data to a file by issuing an HTTP PUT request to the file data resource
    that represents the data for the file. The file binary will be sent in the request body.
    Uploading data to a file creates a new file version in the StackSync datastore and associates the
    uploaded data with the newly created file version.
    """
    content = request.body
    try:
        _, _, file_id, _ = split_path(request.path, 4, 4, False)
    except:
        app.logger.error("StackSync API: data_resource PUT: Wrong resource path: %s path_info: %s", str(400),
                         str(request.path_info))
        return create_error_response(400, "Wrong resource path. Expected /file/:file_id/data")

    app.logger.info('StackSync API: data_resource PUT: path info: %s content length: %i ', str(request.path_info),
                    len(content))

    user_id = request.environ["stacksync_user_id"]

    # We look up the name of file, and full path, to update it.
    #TODO: addChunks true
    message = api_library.get_metadata(user_id, file_id, is_folder=False, include_chunks=True)

    response = create_response(message, status_code=200)
    if not is_valid_status(response.status_int):
        app.logger.error("StackSync API: data_resource PUT: status code: %s. body: %s", str(response.status_int),
                         str(response.body))
        return response

    if len(content) > 0:
        file_metadata = json.loads(message)
        # get the workspace info (includes the container) from the file_id
        workspace_info = api_library.get_workspace_info(user_id, file_id)

        response = create_response(workspace_info, status_code=200)
        if not is_valid_status(response.status_int):
            app.logger.error("StackSync API: data_resource PUT: status code: %s. body: %s", str(response.status_int),
                             str(response.body))
            return response

        workspace_info = json.loads(workspace_info)
        old_chunks = file_metadata['chunks']
	app.logger.info("StackSync API: old_chunks: %s", old_chunks)
        container_name = workspace_info['swift_container']

        #Take the quota information
        quota_limit = long(workspace_info['quota_limit'])
        quota_used = long(workspace_info['quota_used'])
        old_file_size = long(file_metadata['size'])

        #check if the new file exced the quota limit
        quota_used = quota_used - size
        quota_used_after_put = quota_used + long(len(content))
        if (quota_used_after_put > quota_limit):
            return create_error_response(413, "Upload exceeds quota.")

        chunked_file = BuildFile(content, [])
        chunked_file.separate(file_id)
        chunks_diff_remove = list(set(old_chunks) - set(chunked_file.name_list))
        data_handler = DataHandler(app)

        #delete old chunks
        response = data_handler.remove_old_chunks(request.environ, chunks_diff_remove, container_name)
        if not is_valid_status(response.status_int):
            app.logger.error("StackSync API: data_resource PUT: error uploading file chunks: %s path info: %s",
                             str(response.status),
                             str(request.path_info))
            return create_error_response(500, "Could not upload chunks to storage backend.")
        #upload new chunks
        chunks_to_upload = list(set(chunked_file.name_list)-set(old_chunks))
        chunks_already_uploaded =  list(set(chunked_file.name_list)-set(chunks_to_upload))

        chunks = chunked_file.name_list.copy()

        for key in chunks_already_uploaded:
            index = chunked_file.name_list.index(key)
            del chunked_file.name_list[index]
            del chunked_file.chunks[index]
        response = data_handler.upload_file_chunks(request.environ, chunked_file, container_name)

        if not is_valid_status(response.status_int):
            app.logger.error("StackSync API: data_resource PUT: error uploading file chunks: %s path info: %s",
                             str(response.status),
                             str(request.path_info))
            return create_error_response(500, "Could not upload chunks to storage backend.")

        chunks = chunked_file.name_list
        checksum = str((zlib.adler32(content) & 0xffffffff))
        file_size = str(len(content))
        mimetype = magic.from_buffer(content, mime=True)

    else:
        #Empty body
        chunks = []
        checksum = 0
        file_size = 0
        mimetype = 'inode/x-empty'

    message_new_version = api_library.update_data(user_id, file_id, checksum, file_size, mimetype, chunks)

    response = create_response(message_new_version, status_code=201)
    if not is_valid_status(response.status_int):
        app.logger.error("StackSync API: data_resource PUT: error updating data in StackSync Server: %s. body: %s",
                         str(response.status_int),
                         str(response.body))

    return response


def GET(request, api_library, app):
    """
    GET /file/:file_id/data

    Download file data

    To retrieve file data, an application submits an HTTP GET request to the file data resource that
    represents the data for the file.
    """
    try:
        _, _, file_id, _, version, _ = split_path(request.path, 4, 6, False)
    except:
        app.logger.error("StackSync API: data_resource GET: Wrong resource path: %s path_info: %s", str(400),
                         str(request.path_info))
        return create_error_response(400, "Wrong resource path. Expected /file/:file_id/data[/version/:version_id]]")

    app.logger.info('StackSync API: data_resource GET: path info: %s ', str(request.path_info))

    user_id = request.environ["stacksync_user_id"]
    metadata = api_library.get_metadata(user_id, file_id, include_chunks=True,
                                        specific_version=version, is_folder=False)
    response = create_response(metadata, status_code=200)
    if not is_valid_status(response.status_int):
        app.logger.error("StackSync API: data_resource GET: status code: %s. body: %s", str(response.status_int),
                         str(response.body))
        return response

    metadata = json.loads(metadata)

    data_handler = DataHandler(app)

    workspace_info = api_library.get_workspace_info(user_id, file_id)
    response = create_response(workspace_info, status_code=200)
    if not is_valid_status(response.status_int):
        app.logger.error("StackSync API: data_resource GET: status code: %s. body: %s", str(response.status_int),
                         str(response.body))
        return response

    workspace_info = json.loads(workspace_info)
    container_name = workspace_info['swift_container']
    print 'chunks to retrieve', metadata['chunks']
    file_compress_content, status = data_handler.get_chunks(request.environ, metadata['chunks'],
                                                            container_name)

    if is_valid_status(status):
        if len(file_compress_content) > 0:
            joined_file = BuildFile("", file_compress_content)
            joined_file.join()
            headers = {'Content-Type': metadata['mimetype']}
            return HTTPOk(body=joined_file.content, headers=headers)
        elif len(metadata['chunks']) == 0:
            return HTTPOk(body='')
        else:
            app.logger.error("StackSync API: data_resource GET: Unexpected case. File_id: %s.", str(file_id))
            return create_error_response(500, "Could not retrieve file. Please contact an administrator.")
    else:
        app.logger.error("StackSync API: data_resource GET: Cannot retrieve chunks. File_id: %s. Status: %s",
                         str(file_id), str(status))
        return create_error_response(status, "Cannot retrieve chunks from storage backend.")
