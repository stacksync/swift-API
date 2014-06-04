import json, urlparse
from util import *
from stacksync_api_swift.resources.data_handler import DataHandler
import magic
from swift.common.swob import HTTPCreated, HTTPOk
from swift.common.utils import split_path
from stacksync_api_swift.util import create_error_response


def POST(request, api_library, app):
    try:
        params = request.params
        content = request.body

    except:
        return create_error_response(400, "Some problem with parameters.")

    try:
        parent = params.get('parent')
    except:
        parent = None
    try:
        name = params.get('name')
    except:
        name = None

    if not name:
        return create_error_response(400, "It's mandatory to enter a name.")

    if content is not None:
        app.logger.info('StackSync API: file_resource POST: content_length: %s name: %s parent: %s', str(len(content)),
                        str(name), str(parent))

        chunk_maker = BuildFile(content, [])
        chunk_maker.separate()

        url_base = request.environ['PATH_INFO'].replace("/file", "")
        data_handler = DataHandler(app)

        container_response = api_library.get_workspace_info(request.environ["stacksync_user_id"], parent)
        container_response = json.loads(container_response)
        if 'error' in container_response:
            error = container_response["error"]

            app.logger.error('StackSync API: file_resource POST: status: %s description: %s', str(error),
                        str(container_response['description']))

            return create_error_response(error, str(json.dumps(container_response['description'])))

        response = data_handler.upload_file_chunks(request.environ, url_base, chunk_maker, container_response['swift_container'])

        chunks = chunk_maker.hashesList
        checksum = str((zlib.adler32(content) & 0xffffffff))
        file_size = len(content)
        mimetype = magic.from_buffer(content, mime=True)


        if 200 <= response.status_int < 300:
            app.logger.error('StackSync API: file_resource POST: status: %s description: Some problem to upload chunks'
                             ' ', str(response.status_int))
            return response

        message_new_version = api_library.new_file(request.environ["stacksync_user_id"], name, parent, checksum,
                                                   file_size, mimetype, chunks)


        data = json.loads(message_new_version)
        if "error" in data:
            # Create error response
            error = data["error"]
            response = create_error_response(error, str(json.dumps(data['description'])))
            app.logger.error('StackSync API: file_resource POST: status: %s description: %s', str(error),
                        str(data['description']))
        else:
            response = HTTPCreated(body=str(message_new_version))

        return response

    '''Without content'''
    app.logger.info('StackSync API: file_resource POST: content_length: %s name: %s parent: %s', str(0), str(name), str(parent))
    #using new validating module
    message = api_library.new_file(request.environ["stacksync_user_id"], name, parent, None, 0, None, None)

    data = json.loads(message)
    if "error" in data:
        # Create error response
        error = data["error"]
        app.logger.error('StackSync API: file_resource POST: status: %s description: %s', str(error),
                        str(data['description']))
        response = create_error_response(error, str(json.dumps(data['description'])))
    else:
        response = HTTPCreated(body=message)
    return response


def DELETE(request, api_library, app):
    try:
        _, _, file_id = split_path(request.path, 3, 3, False)
    except:
        return create_error_response(400, "It's mandatory to enter a file_id.")
    # get Metadata of the file that had been deleted

    app.logger.info('StackSync API: file_resource DELETE: path info: %s', request.path_info)

    message = api_library.delete_item(request.environ["stacksync_user_id"], file_id)

    data = json.loads(message)
    if "error" in data:
        # Create error response
        error = data["error"]
        response = create_error_response(error, str(json.dumps(data['description'])))
        app.logger.error('StackSync API: file_resource DELETE: status: %s description: %s', str(error),
                        str(data['description']))

    else:
        response = HTTPOk(body=str(message))

    return response


def GET(request, api_library, app):
    try:
        _, _, file_id = split_path(request.path, 3, 3, False)
    except:
        app.logger.error('StackSync API: file_resource GET: status: %s description: %s', str(400),
                         "It's mandatory to enter a file_id.")
        return create_error_response(400, "It's mandatory to enter a file_id.")

    app.logger.info('StackSync API: file_resource GET: path info: %s', request.path_info)


    message = api_library.get_metadata(request.environ["stacksync_user_id"], file_id)

    if not message:
        app.logger.error('StackSync API: file_resource GET: status: %s path info: %s', str(404), request.path_info)
        return create_error_response(404, "File or folder not found at the specified path:" + request.path_info)

    data = json.loads(message)
    if "error" in data:
        # Create error response
        error = data["error"]
        response = create_error_response(error, str(json.dumps(data['description'])))
        app.logger.error('StackSync API: file_resource GET: status: %s description: %s', str(error),
                        str(data['description']))
    else:
        response = HTTPOk(body=str(message))

    return response


def PUT(request, api_library, app):
    try:
        _, _, file_id = split_path(request.path, 3, 3, False)
    except:
        app.logger.error('StackSync API: file_resource PUT: status: %s path info: %s', str(404), request.path_info)
        return create_error_response(400, "It's mandatory to enter a file_id. ")
    try:
        args = urlparse.parse_qs(request.body, 1)
    except:
        app.logger.error('StackSync API: file_resource PUT: status: %s path info: %s', str(404), request.path_info)
        return create_error_response(400, "Some problem with parameters.")
    try:
        parent = args.get('parent')[0]
    except:
        app.logger.error('StackSync API: file_resource PUT: status: %s path info: %s', str(404), request.path_info)
        parent = None
    try:
        name = args.get('name')[0]
    except:
        app.logger.error('StackSync API: file_resource PUT: status: %s path info: %s', str(404), request.path_info)
        name = None

    app.logger.info('StackSync API: file_resource GET: path info: %s', request.path_info)

    message = api_library.put_metadata(request.environ["stacksync_user_id"], file_id, name, parent)

    data = json.loads(message)
    if "error" in data:
        # Create error response
        error = data["error"]
        response = create_error_response(error, str(json.dumps(data['description'])))
        app.logger.error('StackSync API: file_resource PUT: status: %s description: %s', str(error),
                        str(data['description']))
    else:
        response = HTTPCreated(body=str(message))

    return response
