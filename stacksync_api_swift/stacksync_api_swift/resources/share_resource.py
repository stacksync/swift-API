from swift.common.utils import split_path
from stacksync_api_swift.resources.resource_util import create_response, is_valid_status, create_error_response
import json

def POST(request, api_library, app):
    try:
        _, _, folder_id, _ = split_path(request.path, 4, 4, False)
    except:
        app.logger.error("StackSync API: share_resource POST: Wrong resource path: %s path_info: %s", str(400),
                         str(request.path_info))
        return create_error_response(400, "Wrong resource path. Expected /folder/:folder_id/sahre")

    content = request.body
    content = json.loads(content)
    if len(content) > 0:
        message = api_library.share_folder(request.environ["stacksync_user_id"], folder_id, content)
        response = create_response(message, status_code=201)
        return response
    else:
        app.logger.error("StackSync API: share_resource POST: Bad request - Empty content")
        return create_error_response(400, "No addressee found.")

