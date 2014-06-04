from swift.common.utils import split_path
from swift.common.swob import HTTPOk
from stacksync_api_swift.util import create_error_response

def GET(request, api_library, app):

    try:
        include_deleted = request.params.get('include_deleted')[0]
        if not include_deleted:
            include_deleted = False
    except:
        include_deleted = False
    try:    
        _, _, folder_id, _ = split_path(request.path, 4, 4, False)
    except:
        return create_error_response(400, "Some problem with path")

    app.logger.info('StackSync API: contents_resource GET: path info: %s ', str(request.path_info))
    message = api_library.get_folder_contents(request.environ["stacksync_user_id"], folder_id, include_deleted)
    if not message:
        app.logger.error('StackSync API: contents_resource GET: status: %s path_info: %s',
                                  str(404), str(request.path_info))
        return create_error_response(404, "File or folder not found at the specified path:" + request.path)


    return HTTPOk(body=message)
