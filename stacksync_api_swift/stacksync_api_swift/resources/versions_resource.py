from swift.common.utils import split_path
from stacksync_api_swift.resources.resource_util import create_response, is_valid_status, create_error_response


def GET(request, api_library, app):
    """
    GET /file/:file_id/[versions|version/:version_id]

    Get file versions and version metadata

    To retrieve information about a file version, an application submits an HTTP GET request
    to the file version resource.
    """

    try:    
        _, _, file_id, _, version = split_path(request.path, 4, 5, False)
    except:
        app.logger.error("StackSync API: file_resource DELETE: Wrong resource path: %s path_info: %s", str(400),
                         str(request.path_info))
        return create_error_response(400, "Wrong resource path. Expected /file/:file_id")

        app.logger.info('StackSync API: versions_resource GET: error: 400, path info: %s ', str(request.path_info))
        return create_error_response(400, "Some problem with path.")

    app.logger.info('StackSync API: versions_resource GET: path info: %s ', str(request.path_info))

    user_id = request.environ["stacksync_user_id"]

    if not version:
        # if no version is given, return the list of versions
        message = api_library.get_versions(user_id, file_id)
        response = create_response(message, status_code=200)
        if not is_valid_status(response.status_int):
            app.logger.error("StackSync API: versions_resource GET: error getting versions of file: %s.",
                             str(file_id))
    else:
        # if a version is given, return metadata about that specific version
        message = api_library.get_metadata(user_id, file_id, specific_version=version, is_folder=False)
        response = create_response(message, status_code=200)
        if not is_valid_status(response.status_int):
            app.logger.error("StackSync API: versions_resource GET: error getting version of file %s and version %s.",
                             str(file_id), str(version))

    return response
