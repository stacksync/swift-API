from swift.common.utils import split_path
from stacksync_api_swift.resources.resource_util import create_response, is_valid_status, create_error_response


def GET(request, api_library, app):
    """
    GET /folder/:file_id/contents.

    Query parameters:
        - include_deleted: (Optional) False by default. If it is set to true, then response will
                            include metadata of deleted objects.

    Get folder content metadata

    To retrieve information about a folder, an application submits an HTTP GET request
    to the folder resource that represents the folder. To get information about the root
    folder, users must set the folder ID to “0” (i.e. /folder/0/contents).
    """

    try:
        _, _, folder_id, _ = split_path(request.path, 4, 4, False)
    except:
        app.logger.error("StackSync API: contents_resource GET: Wrong resource path: %s path_info: %s", str(400),
                         str(request.path_info))
        return create_error_response(400, "Wrong resource path. Expected /folder/:folder_id/contents")

    try:
        include_deleted = request.params.get('include_deleted')
        if not include_deleted:
            include_deleted = False
    except:
        include_deleted = False

    app.logger.info('StackSync API: contents_resource GET: path info: %s ', str(request.path_info))

    user_id = request.environ["stacksync_user_id"]

    message = api_library.get_folder_contents(user_id, folder_id, include_deleted)

    response = create_response(message, status_code=200)
    if not is_valid_status(response.status_int):
        app.logger.error("StackSync API: file_resource POST: error updating data in StackSync Server: %s. body: %s",
                         str(response.status_int),
                         str(response.body))

    return response