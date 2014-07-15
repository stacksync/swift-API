from swift.common.utils import split_path
from stacksync_api_swift.resources.resource_util import create_response, is_valid_status, create_error_response
import json

def GET(request, api_library, app):
    try:
        _, _, folder_id, _ = split_path(request.path, 4, 4, False)
    except:
        app.logger.error("StackSync API: share_resource GET: Wrong resource path: %s path_info: %s", str(400),
                         str(request.path_info))
        return create_error_response(400, "Wrong resource path. Expected /folder/:folder_id/members")

    message = api_library.get_folder_members(request.environ["stacksync_user_id"], folder_id)
    response = create_response(message, status_code=200)
    if not is_valid_status(response.status_int):
        app.logger.error("StackSync API: folder members GET: error getting folder members in StackSync Server: %s.",
                         str(response.status_int))
    return response

