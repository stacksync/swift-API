import urlparse
from swift.common.swob import HTTPCreated, HTTPOk
from swift.common.utils import split_path
from swift_server.util import create_error_response


def POST(request, api_library, app):
    try:
        args = urlparse.parse_qs(request.body, 1)
    except:
		app.logger.error('StackSync API: Could not parse arguments: %s ', str(request.body))
        return create_error_response(400, "Could not parse arguments.")
  
    try:
        parent = args.get('parent')[0]
    except:
        parent = None
    try:
        name = args.get('name')[0]
    except:
        name = None

    app.logger.info('StackSync API: folder_resource POST: path info: %s ', str(request.path_info))

    if not name:
        app.logger.error("StackSync API: folder_resource POST: error: 400. description: Folder name not found.")
        return create_error_response(400, "Folder name not found.")
    
    message = api_library.new_folder(request.environ["stacksync_user_id"], name, parent)

    return HTTPCreated(body=message)

def DELETE(request, api_library, app):

    try:    
        _, _, folder_id = split_path(request.path, 3, 3, False)
    except:
        app.logger.error("StackSync API: folder_resource DELETE: error: 400. description: Folder ID not found.")
        return create_error_response(400, "Folder ID not found.")

    app.logger.info('StackSync API: folder_resource DELETE: path info: %s ', str(request.path_info))

    message = api_library.delete_item(request.environ["stacksync_user_id"], folder_id)
    if not message:
        app.logger.error("StackSync API: folder_resource DELETE: error: %s path_info: %s", str(404),
                         str(request.path_info))
        return create_error_response(404, "Folder not found:")

    return HTTPOk(body=message)

def GET(request, api_library, app):

    try:    
        _, _, folder_id = split_path(request.path, 2, 3, False)
    except:
        app.logger.error("StackSync API: folder_resource DELETE: error: 400. description: Folder ID not found.")
        return create_error_response(400, "Folder ID not found.")

    app.logger.info('StackSync API: folder_resource GET: path info: %s ', str(request.path_info))

    message = api_library.get_metadata(request.environ["stacksync_user_id"], folder_id)

    if not message:
        app.logger.error("StackSync API: folder_resource GET: error: %s path_info: %s", str(404),
                         str(request.path_info))
        return create_error_response(404, "Folder not found")
           

    return HTTPOk(body=message)

def PUT(request, api_library, app):

    try:
        _, _, folder_id = split_path(request.path, 3, 3, False)
    except:
        app.logger.error("StackSync API: folder_resource PUT: error: 400. description: Folder ID not found.")
        return create_error_response(400, "Folder ID not found.")
    try:
        args = urlparse.parse_qs(request.body, 1)
    except:
        app.logger.error("StackSync API: folder_resource DELETE: error: 400. description: Could not parse body arguments.")
        return create_error_response(400, "Could not parse body arguments.")
    try:
        parent = args.get('parent')[0]
    except:
        parent = None
    try:
        name = args.get('name')[0]
    except:
        name = None

    app.logger.info('StackSync API: folder_resource PUT: path info: %s ', str(request.path_info))

    message = api_library.put_metadata(request.environ["stacksync_user_id"], folder_id, name, parent)

    return HTTPCreated(body=message)
