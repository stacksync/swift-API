from swift.common.utils import split_path
from stacksync_api_swift.resources.resource_util import create_response, is_valid_status, create_error_response
import json


def POST(request, api_library, app):
    """
    POST /folder/:folder_id

    Create a folder

    An application can create a folder by issuing an HTTP POST request to the URL of the containing folder
    resource. In addition, the application needs to provide as input, JSON that identifies the display name
    of the folder to be created.
    """

    try:
        args = json.loads(request.body)
    except:
        app.logger.error("StackSync API: folder_resource POST: Could not parse body parameters. Body %s",
                         str(request.body))
        return create_error_response(400, "Wrong resource path. Expected /folder/:folder_id")

    try:
        parent = args['parent']
    except KeyError:
        parent = None
    try:
        name = args['name']
    except KeyError:
        name = None

    app.logger.info(
        'StackSync API: folder_resource POST: path info: %s, body=%s' % (str(request.path_info), request.body))

    if not name:
        app.logger.error("StackSync API: folder_resource POST: error: 400. description: Folder name not set.")
        return create_error_response(400, "Folder name not set.")

    user_id = request.environ["stacksync_user_id"]

    message = api_library.new_folder(user_id, name, parent)

    response = create_response(message, status_code=201)
    if not is_valid_status(response.status_int):
        app.logger.error("StackSync API: folder_resource POST: error creating folder in StackSync Server: %s.",
                         str(response.status_int))
    return response


def DELETE(request, api_library, app):
    """
    DELETE /folder/:folder_id

    Delete a folder

    An application can permanently delete a folder by issuing an HTTP DELETE request to the URL of the
    folder resource. It's a good idea to precede DELETE requests like this with a caution note in your
    application's user interface.
    """

    try:
        _, _, folder_id = split_path(request.path, 3, 3, False)
    except:
        app.logger.error("StackSync API: folder_resource DELETE: Wrong resource path: %s path_info: %s", str(400),
                         str(request.path_info))
        return create_error_response(400, "Wrong resource path. Expected /folder/:folder_id")

    app.logger.info('StackSync API: folder_resource DELETE: path info: %s ', str(request.path_info))
    user_id = request.environ["stacksync_user_id"]

    message = api_library.delete_item(user_id, folder_id)

    response = create_response(message, status_code=200)
    if not is_valid_status(response.status_int):
        app.logger.error("StackSync API: folder_resource DELETE: error deleting folder in StackSync Server: %s.",
                         str(response.status_int))
    return response


def GET(request, api_library, app):
    """
    GET /folder/:folder_id

    Get folder metadata

    To retrieve information about a folder, an application submits an HTTP GET request to the folder
    resource that represents the folder. To get information about the root folder, users must set the
    ID to “0” (i.e. /folder/0).
    """

    try:
        _, _, folder_id = split_path(request.path, 2, 3, False)
    except:
        app.logger.error("StackSync API: folder_resource GET: Wrong resource path: %s path_info: %s", str(400),
                         str(request.path_info))
        return create_error_response(400, "Wrong resource path. Expected /folder/:folder")

    app.logger.info('StackSync API: folder_resource GET: path info: %s ', str(request.path_info))
    user_id = request.environ["stacksync_user_id"]

    message = api_library.get_metadata(user_id, folder_id)

    response = create_response(message, status_code=200)
    if not is_valid_status(response.status_int):
        app.logger.error("StackSync API: folder_resource DELETE: error deleting folder in StackSync Server: %s.",
                         str(response.status_int))
    return response


def PUT(request, api_library, app):
    """
    PUT /folder/:folder_id

    Body parameters (JSON encoded):
        - name: (Optional) The user-visible name of the folder.
        - parent: (Optional) ID of the folder where the folder is going to be moved. If parent is set
                    to '0' the folder will be moved to the root folder.

    Update folder metadata

    An application can update various attributes of a folder by issuing an HTTP PUT request to the URL
    that represents the folder resource. In addition, the app needs to provide as input, JSON that
    identifies the new attribute values for the folder. Upon receiving the PUT request, the StackSync
    service examines the input and updates any of the attributes that have been modified.
    """

    try:
        _, _, folder_id = split_path(request.path, 3, 3, False)
    except:
        app.logger.error("StackSync API: folder_resource PUT: Wrong resource path: %s path_info: %s", str(400),
                         str(request.path_info))
        return create_error_response(400, "Wrong resource path. Expected /folder/:folder")

    try:
        params = json.loads(request.body)
    except:
        app.logger.error('StackSync API: folder_resource PUT: status: %s path info: %s', str(404), request.path_info)
        return create_error_response(400, "Could not decode body parameters.")

    try:
        parent = params['parent']
    except KeyError:
        parent = None
    try:
        name = params['name']
    except KeyError:
        name = None

    app.logger.info('StackSync API: folder_resource PUT: path info: %s ', str(request.path_info))
    user_id = request.environ["stacksync_user_id"]

    message = api_library.put_metadata(user_id, folder_id, name, parent)

    response = create_response(message, status_code=200)
    if not is_valid_status(response.status_int):
        app.logger.error("StackSync API: folder_resource DELETE: error deleting folder in StackSync Server: %s.",
                         str(response.status_int))
    return response
