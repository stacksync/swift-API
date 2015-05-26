from swift.common.utils import split_path
from stacksync_api_swift.resources.data_handler import DataHandler
from stacksync_api_swift.resources.data_util import BuildFile
from stacksync_api_swift.resources.resource_util import create_response, is_valid_status, create_error_response
import json
import zlib
import magic


def POST(request, api_library, app):
    """
    POST /file

    Query arguments:
        - name: The user-visible name of the file to be created.
        - parent: (Optional) ID of the folder where the file is going to be created.
                    If no ID is given or if ID is '0', it will use the top-level (root) folder.

    Create a file

    An application can create a file by issuing an HTTP POST request. The application needs to provide
    the file binary in the body and the file name as a query argument. Optionally, it can also provide
    the parent argument to locate the file in a specific folder. Otherwise, the file will be placed in
    the root folder.
    """

    try:
        params = request.params
        content = request.body
    except:
        app.logger.error('StackSync API: file_resource POST: Could not obtain input parameters')
        return create_error_response(400, "Could not obtain input parameters.")

    try:
        parent = params.get('parent')
    except:
        parent = None
    try:
        name = params.get('name')
    except:
        name = None

    if not name:
        app.logger.error('StackSync API: file_resource POST: Invalid file name.')
        return create_error_response(400, "Invalid file name.")

    user_id = request.environ["stacksync_user_id"]

    if len(content) > 0:
        app.logger.info('StackSync API: file_resource POST: content_length: %s name: %s parent: %s', str(len(content)),
                        str(name), str(parent))

        workspace_info = api_library.get_workspace_info(user_id, parent)
        response = create_response(workspace_info, status_code=200)
        if not is_valid_status(response.status_int):
            app.logger.error("StackSync API: file_resource POST: status code: %s. body: %s", str(response.status_int),
                             str(response.body))
            return response

        workspace_info = json.loads(workspace_info)
        container_name = workspace_info['swift_container']
        #Take the quota information
        quota_used = long(workspace_info['quota_used'])
        quota_limit = long(workspace_info['quota_limit'])

        #check if the new file exced the quota limit
        quota_used_after_put = long(quota_used) + long(len(content))
        if (quota_used_after_put > quota_limit):
            return create_error_response(413, "Upload exceeds quota.")

        chunked_file = BuildFile(content, [])
        chunked_file.separate()

        data_handler = DataHandler(app)

        response = data_handler.upload_file_chunks(request.environ, chunked_file, container_name)

        chunks = chunked_file.chunk_dict.keys()
        checksum = str((zlib.adler32(content) & 0xffffffff))
        file_size = len(content)
        mimetype = magic.from_buffer(content, mime=True)

        if not is_valid_status(response.status_int):
            app.logger.error("StackSync API: file_resource POST: error uploading file chunks: %s path info: %s",
                             str(response.status),
                             str(request.path_info))
            return response

    else:
        # Empty body
        checksum = 0
        file_size = 0
        mimetype = 'inode/x-empty'
        chunks = []

    message_new_version = api_library.new_file(user_id, name, parent, checksum, file_size, mimetype, chunks)
    response = create_response(message_new_version, status_code=201)
    if not is_valid_status(response.status_int):
        app.logger.error("StackSync API: file_resource POST: error updating data in StackSync Server: %s. body: %s",
                         str(response.status_int),
                         str(response.body))

    return response


def DELETE(request, api_library, app):
    """
    DELETE /file/:file_id

    Delete a file

    An application can delete a file by issuing an HTTP DELETE request to the URL of the file resource.
    It's a good idea to precede DELETE requests like this with a caution note in your application's user
    interface.
    """

    try:
        _, _, file_id = split_path(request.path, 3, 3, False)
    except:
        app.logger.error("StackSync API: file_resource DELETE: Wrong resource path: %s path_info: %s", str(400),
                         str(request.path_info))
        return create_error_response(400, "Wrong resource path. Expected /file/:file_id")

    app.logger.info('StackSync API: file_resource DELETE: path info: %s', request.path_info)
    user_id = request.environ["stacksync_user_id"]

    message = api_library.get_metadata(user_id, file_id, is_folder=False, include_chunks=True)

    response = create_response(message, status_code=200)
    if not is_valid_status(response.status_int):
        app.logger.error("StackSync API: data_resource DELETE: status code: %s. body: %s", str(response.status_int),
                         str(response.body))
        return response
    workspace_info = api_library.get_workspace_info(user_id, file_id)

    response = create_response(workspace_info, status_code=200)
    if not is_valid_status(response.status_int):
        app.logger.error("StackSync API: data_resource PUT: status code: %s. body: %s", str(response.status_int),
                             str(response.body))
        return response

    workspace_info = json.loads(workspace_info)
    data_handler = DataHandler(app)
    file_metadata = json.loads(message)
    container_name = workspace_info['swift_container']
    response = data_handler.remove_old_chunks(request.environ, file_metadata['chunks'], container_name)
    response = create_response(message, status_code=200)
    if not is_valid_status(response.status_int):
        app.logger.error("StackSync API: data_resource DELETE: status code: %s. body: %s", str(response.status_int),
                         str(response.body))
        return response

    message_delete = api_library.delete_item(user_id, file_id, is_folder=False)

    response = create_response(message_delete, status_code=200)
    if not is_valid_status(response.status_int):
        app.logger.error("StackSync API: file_resource DELETE: error deleting file in StackSync Server: %s.",
                         str(response.status_int))
    return response


def GET(request, api_library, app):
    """
    GET /file/:file_id

    Get file's metadata

    To retrieve information about a file, an application submits an HTTP GET request to the file
    resource that represents the file.
    """

    try:
        _, _, file_id = split_path(request.path, 3, 3, False)
    except:
        app.logger.error("StackSync API: file_resource GET: Wrong resource path: %s path_info: %s", str(400),
                         str(request.path_info))
        return create_error_response(400, "Wrong resource path. Expected /file/:file_id")

    app.logger.info('StackSync API: file_resource GET: path info: %s', request.path_info)
    user_id = request.environ["stacksync_user_id"]

    message = api_library.get_metadata(user_id, file_id, is_folder=False)

    response = create_response(message, status_code=200)
    if not is_valid_status(response.status_int):
        app.logger.error("StackSync API: file_resource GET: Error getting file metadata from StackSync Server: %s.",
                         str(response.status_int))
    return response


def PUT(request, api_library, app):
    """
    PUT /file/:file_id

    Body parameters (JSON encoded):
        - name: (Optional) The user-visible name of the file to be created.
        - parent: (Optional) ID of the folder where the file or folder is going to be moved. If ID is
                    set to '0', it will be moved the top-level (root) folder.

    Update file metadata

    An application can update various attributes of a file by issuing an HTTP PUT request to the URL that
    represents the file resource. In addition, the app needs to provide as input, JSON that identifies the
    new attribute values for the file. Upon receiving the PUT request, the StackSync service examines the
    input and updates any of the attributes that have been modified.
    """

    try:
        _, _, file_id = split_path(request.path, 3, 3, False)
    except:
        app.logger.error("StackSync API: file_resource PUT: Wrong resource path: %s path_info: %s", str(400),
                         str(request.path_info))
        return create_error_response(400, "Wrong resource path. Expected /file/:file_id")

    try:
        params = json.loads(unicode(request.body, 'iso-8859-15'))
    except:
        app.logger.error('StackSync API: file_resource PUT: status: %s path info: %s', str(404), request.path_info)
        return create_error_response(400, "Could not decode body parameters.")

    try:
        parent = params['parent']
    except KeyError:
        parent = None
    try:
        name = params['name']
    except KeyError:
        name = None

    app.logger.info('StackSync API: file_resource PUT: path info: %s', request.path_info)
    user_id = request.environ["stacksync_user_id"]

    message = api_library.put_metadata(user_id, file_id, name, parent)

    response = create_response(message, status_code=200)
    if not is_valid_status(response.status_int):
        app.logger.error("StackSync API: file_resource PUT: error updateing file in StackSync Server: %s.",
                         str(response.status_int))
    return response
